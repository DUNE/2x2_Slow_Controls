/*
  devSnmp.h

  by J.Priller  NSCL/FRIB
*/
#ifndef	DEVSNMP_H
#define	DEVSNMP_H

#include <math.h>
#include <devSup.h>
#include <menuScan.h>
#include <dbScan.h>
#include <epicsTime.h>
#include <epicsThread.h>

#include <net-snmp/net-snmp-config.h>
#include <net-snmp/net-snmp-includes.h>

#include "requireNetSNMPversion.h"

//
// define default maximum for oids per get request
// can be overridden on a per-host basis by IOC shell call to
// devSnmpSetMaxOidsPerReq
//
// Wiener/ISEG crates can generally handle 50, but we use 32 as
// a default because not all SNMP devices can handle that many
//
#define DEFAULT_MAX_OIDS_PER_REQ  32

typedef uint32_t SNMP_UINT32;
typedef uint64_t SNMP_UINT64;
typedef int32_t  SNMP_INT32;
typedef int64_t  SNMP_INT64;

struct __oid {
  const char *Name;
  oid Oid[MAX_OID_LEN];
  size_t OidLen;
};

//
// format of INP/OUT lines is
//    '@host community oidname mask maxdatalength [set_format/special]'
//
//  host, community and oidname define a unique oid (devSnmp_oid)
//  mask, datalen, set_format/special are particular to PVs (devSnmp_pv)
//
typedef struct {
  char host[128];
  char community[128];
  char oidStr[128];
} configDataOid;

typedef struct {
  char mask[128];
  char specialStr[128];
  int  data_len;
  char set_type;
  long special_flags;
} configDataPV;

#define V3_TXT_LEN 512
typedef struct {
  char   securityName[V3_TXT_LEN];
  char   authPassPhrase[V3_TXT_LEN];
  char   privPassPhrase[V3_TXT_LEN];
  char   context[V3_TXT_LEN];
  oid   *securityAuthProto;
  size_t securityAuthProtoLen;
  oid   *securityPrivProto;
  size_t securityPrivProtoLen;
  int    securityLevel;
} devSnmp_v3params;

typedef struct snmp_session SNMP_SESSION;
typedef struct snmp_pdu SNMP_PDU;
typedef struct __oid OID;

// forward declarations
class devSnmp_manager;
class devSnmp_host;
class devSnmp_group;
class devSnmp_oid;
class devSnmp_pv;
class devSnmp_session;
class devSnmp_getTransaction;
class devSnmp_setTransaction;
class devSnmp_hostversion;

typedef long (*DEVSNMP_DEVFUNC)(devSnmp_pv *pPV);

// needed to cast to this if c++ wants to call RECSUPFUN functions in EPICS base
typedef long (*RECSUPFUN_VOID_PTR)(void *ptr);

//----------------------------------------------------------------------
// define a simple class for maintaining a dynamic list of pointers
typedef int (*POINTERLIST_COMPARE_PROC)(void *p1, void *p2);
class snmpPointerList
{
  public:
    snmpPointerList(int initialCount = 1024, int extendCount = 1024);
    virtual ~snmpPointerList(void);
    virtual void append(void *ptr);
    virtual int count(void);
    virtual void *itemAt(int idx);
    virtual void *removeItemAt(int idx);
    virtual void sort(POINTERLIST_COMPARE_PROC proc);
    virtual void resize(int newSize);
    virtual void *context(void);
    virtual void setContext(void *newcontext);
    virtual void **rawArray(void);

  protected:
    int    delta;
    int    currSize;
    int    currCount;
    void **pPtrList;
    void  *_context;
};
//--------------------------------------------------------------------
// define a class for handling the ordering of OID scans via weights
typedef struct {
  int              pollMSec;
  snmpPointerList *pList;
  int              tail;
  // these only guaranteed to be valid between transactionBuildStart..End calls:
  int              start;
  int              topPollWeight;
  int              count;
  devSnmp_oid     **rawArray;
} readBinListItem;

class snmpWeightCollection
{
  public:
    snmpWeightCollection(void);
    virtual ~snmpWeightCollection(void);

    virtual void addOID(devSnmp_oid *pOid);
    virtual devSnmp_oid *topOID(void);
    virtual void nextOID(void);
    virtual void binChange(void);
    virtual void transactionBuildStart(void);
    virtual void transactionBuildEnd(void);

  protected:
    epicsMutexId mutex;
    bool redoBins;
    bool inBuild;
    snmpPointerList *binList;
    snmpPointerList *oidList;
    void createBins(void);
    void deleteBins(void);
    readBinListItem *findBin(int pollMSec);

  private:
    // these only guaranteed to be valid between transactionBuildStart..End calls:
    int binIdx;
    int binCount;
    readBinListItem **binArray;
};
//--------------------------------------------------------------------
// define a class for storing time info, measuring elapsed time
class snmpTimeObject
{
  public:
    snmpTimeObject(void);
    virtual ~snmpTimeObject(void);
    void start(epicsTimeStamp *pnow);
    void clear(void);
    bool started(void);
    double elapsedSeconds(epicsTimeStamp *pnow);
    long elapsedMilliseconds(epicsTimeStamp *pnow);
    void toDateTimeString(char *str);

  protected:
    epicsTimeStamp lastStarted;
};
//----------------------------------------------------------------------
class devSnmp_setting
{
  public:
    devSnmp_setting(char set_type, char *set_string);
    virtual ~devSnmp_setting(void);
    const char *setString(void);
    char setType(void);
  protected:
    char settingType;
    char *settingString;
};
//----------------------------------------------------------------------

/*
  NET-SNMP changed somewhere around version 5.6 to assume the callback_magic
  field of snmp_session was a pointer to 'struct synch_state'.

  We therefore define a devSnmp_magic structure that includes a struct
  synch_state as its first element, and whatever content we want (such as the
  pointer to a netSnmp_session) comes after that.
*/
typedef struct {
  struct synch_state SS;
  unsigned char padding[64];
  devSnmp_session *sessionObject;
} devSnmp_magic;

class devSnmp_session
/* one of these structures exists for each active session, GET or SET,
   kept track of in devSnmp_host item's activeSessionList list */
{
  public:
    devSnmp_session(devSnmp_manager *pMgr, devSnmp_group *pGroup, bool is_set);
    virtual ~devSnmp_session(void);
    bool open(SNMP_SESSION *psess);
    bool send(void);
    void close(void);
    int itemCount(void);
    bool isCompleted(void);
    bool wasSent(void);
    bool isSetting(void);
    double secondsSinceCreated(epicsTimeStamp *pnow);
    double secondsSinceSent(epicsTimeStamp *pnow);
    long millisecondsSinceCreated(epicsTimeStamp *pnow);
    long millisecondsSinceSent(epicsTimeStamp *pnow);

    void addReading(devSnmp_oid *pOID);
    void addSetting(devSnmp_oid *pOID, devSnmp_setting *pSet);

    int replyProcessing(int op, SNMP_SESSION *sp, int reqId, SNMP_PDU *pdu);

    SNMP_SESSION *getSession(void);

  protected:
    devSnmp_magic    ourMagic;
    devSnmp_manager *pOurMgr;
    devSnmp_group   *pOurGroup;
    SNMP_SESSION    *session;
    SNMP_PDU        *pdu;
    snmpTimeObject   timeStarted;
    snmpTimeObject   timeSent;
    snmpPointerList *oidList;
    bool             is_setting;
    bool             completed;
    bool             sent;
    bool             tried_send;
};
//----------------------------------------------------------------------
class devSnmp_transaction
// base class for SNMP transactions we'll perform (get and set)
{
  public:
    devSnmp_transaction(bool isSet);
    virtual ~devSnmp_transaction(void);
    bool isSetting(void);
    long millisecondsSinceCreated(epicsTimeStamp *pnow);
    virtual devSnmp_session *createSession(void) = 0;

  protected:
    bool       is_set;
    snmpTimeObject createTime;
};
//----------------------------------------------------------------------
class devSnmp_getTransaction : public devSnmp_transaction
// class to hold data for an SNMP 'get' transaction'
// allows multiple elements per request, up to MaxItems
{
  public:
    devSnmp_getTransaction(int MaxItems);
    virtual ~devSnmp_getTransaction(void);
    void addOID(devSnmp_oid *pOID);
    bool isFull(void);
    int count(void);
    virtual devSnmp_session *createSession(void);

  protected:
    snmpPointerList *oidList;
    int ourMaxItems;
};
//----------------------------------------------------------------------
class devSnmp_setTransaction : public devSnmp_transaction
/*
   class to hold data for an SNMP 'set' transaction'
   allows only one element per request, as SNMP set replies don't return
   which element triggered the error if one of them causes an error
*/
{
  public:
    devSnmp_setTransaction(devSnmp_oid *pOID);
    virtual ~devSnmp_setTransaction(void);
    virtual devSnmp_session *createSession(void);
    bool sameOid(devSnmp_setTransaction *pOID);

  protected:
    devSnmp_oid     *ourOID;
    devSnmp_setting *ourSetting;
};
//----------------------------------------------------------------------

typedef struct {
    bool    valid;
    char   *read_string;
    bool    has_double;
    double  read_double;
    bool    has_long;
    long    read_long;
} _oid_reading;

class devSnmp_oid
// one of these objects exists for each unique OID (group + OID-name)
{
  friend class snmpWeightCollection;

  public:
    devSnmp_oid(devSnmp_manager *pMgr,
                devSnmp_group   *pGroup,
                configDataOid   *pOidBase,
                OID             *pOid,
                bool            *okay);
    virtual ~devSnmp_oid(void);

    bool hasReading(void);
    bool hasReadingDouble(void);
    bool hasReadingLong(void);
    bool getValueDouble(double *value);
    bool getValueLong(long *value);
    bool getRawValueString(char *str, int maxsize);

    void queueUpdate(void);
    void periodicProcessing(epicsTimeStamp *pnow);

    int getDataLength(void);
    void setDataLength(int length);

    double pollsPerSecond(void);
    long pollAgeMSec(void);
    int getPollMSec(void);
    void setPollMSec(int msec);

    void set(char set_type, char *str);
    bool needsSet(void);
    devSnmp_setting *getNextSetting(void);
    void debugSetStart();
    void debugSetProgress(const char * msg);
    void debugSetEnd();

    long recalcPollWeight(epicsTimeStamp *pnow);
    long getPollWeight(void);

    void setGetQueued(bool state);

    devSnmp_manager *getManager(void);
    devSnmp_group *getGroup(void);

    OID *getOid(void);
    int badFlag(void);

    void settingSendStatus(bool state);
    void readingSendStatus(bool state);

    int replyProcessing(devSnmp_session       *pSession,
                        int                    op,
                        long                   errCode,
                        netsnmp_variable_list *var);

    const char *hostName(void);
    const char *communityName(void);
    const char *oidName(void);

    void zeroCounters(void);
    void report(int level, char *match);
    bool reportMatchAny(char *match);
    void debugDump(void);

    const char *errorString(void);

  protected:
    devSnmp_manager  *pOurMgr;
    devSnmp_group    *pOurGroup;
    OID               oid;
    configDataOid     oidBase;
    int               data_len;
    epicsMutexId      valMutex;
    epicsMutexId      setMutex;
    devSnmp_setting  *settingToSend;
    int               flagged_read_bad;
    snmpTimeObject    pollStart;
    snmpTimeObject    lastSetSent;
    snmpTimeObject    lastPollSent;
    snmpTimeObject    lastPollReply;
    unsigned long     pollSendCount;
    unsigned long     pollReplyCount;
    unsigned long     errorCount;
    unsigned long     setCount;
    bool              queued_for_get;
    bool              validFlag;
    long              pollWeight;
    long              pollMSec;
    unsigned long     compFailures;
    char              lastError[256];
    bool              setDebugging;
    snmpTimeObject    debugSetTime;
    _oid_reading      reading;

    void clearData(void);
    void storeData(netsnmp_variable_list *var);

    int setReplyProcessing(devSnmp_session       *pSession,
                           int                    op,
                           long                   errCode,
                           netsnmp_variable_list *var);

    int readReplyProcessing(devSnmp_session       *pSession,
                            int                    op,
                            long                   errCode,
                            netsnmp_variable_list *var);
};
//----------------------------------------------------------------------
class devSnmp_pv
// one of these objects exists for each PV
{
  public:
    devSnmp_pv(devSnmp_manager *pMgr,
               devSnmp_group   *pGroup,
               struct dbCommon *pRecord,
               devSnmp_oid     *pOID,
               configDataPV    *pOidExtra,
               bool            *okay);
    virtual ~devSnmp_pv(void);

    bool hasValue();
    bool getValueString(char *str, int maxsize);
    bool getValueDouble(double *value);
    bool getValueLong(long *value);
    bool getRawValueString(char *str, int maxsize);

    void periodicProcessing(epicsTimeStamp *pnow);
    void processRecord(bool asyncUpdate = false);
    bool doingProcess(void);

    void set(char *str);
    bool wasSetRecently(void);
    char getSetType(void);
    void debugSetStart();
    void debugSetProgress(const char * msg);
    void debugSetEnd();

    double pollsPerSecond(void);
    int getPollMSec(void);
    void setPollMSec(int msec);

    void setPeriodicCallback(DEVSNMP_DEVFUNC procFunc, double seconds);

    void queueUpdate(void) { if (pOurOID) pOurOID->queueUpdate(); }

    const char *recordName(void);
    struct dbCommon *record(void);

    int getDataLength(void);
    void setDataLength(int length);

    void zeroCounters(void);
    void report(int level, char *match);
    bool reportMatchAny(char *match);
    void debugDump(void);

    const char *errorString(void);

    const configDataPV *configData(void);
    long configFlags(void);

    devSnmp_oid* OID() { return pOurOID; }

  protected:
    devSnmp_manager  *pOurMgr;
    devSnmp_group    *pOurGroup;
    devSnmp_oid      *pOurOID;
    struct dbCommon  *pOurRecord;
    DEVSNMP_DEVFUNC   pPeriodicFunction;
    long              periodicMSec;
    snmpTimeObject    lastSetSent;
    snmpTimeObject    lastPeriodicFuncCall;
    bool              in_rec_process;
    configDataPV      oidExtra;
    unsigned long     setCount;
    int               pollMSec;
    char              lastError[256];
};
//----------------------------------------------------------------------
class devSnmp_group
/* one of these structures exists for each host/community
   (things for which we can pack GET requests into one session) */
{
  public:
    devSnmp_group(devSnmp_manager *pMgr, devSnmp_host *host, char *community, bool *okay);
    virtual ~devSnmp_group(void);
    devSnmp_pv *addPV(configDataOid    *base,
                      configDataPV     *extra,
                      OID              *oid,
                      struct dbCommon  *pRecord);
    void processing(epicsTimeStamp *pnow);

    const char *hostName(void);
    const char *communityName(void);
    int snmpVersion(void);

    void setMaxOidsPerReq(int maxoids);
    int getMaxOidsPerReq(void);

    void zeroCounters(void);
    void report(int level, char *match);
    bool reportMatchAny(char *match);

    void sessionSent(int state);
    void sessionGotReply(devSnmp_session *pSession);
    void sessionGotError(devSnmp_session *pSession);

    SNMP_SESSION *getBaseSession(void);

    void sessionRetriesChange(void);
    void sessionTimeoutChange(void);

    void updatePVs(devSnmp_oid *pOid);

  protected:
    devSnmp_manager      *pOurMgr;
    devSnmp_host         *pOurHost;
    SNMP_SESSION         *base_session;
    snmpPointerList      *pvList;
    snmpPointerList      *oidList;
    snmpWeightCollection *weightCollection;
    long                  bestReplyMsec;
    long                  worstReplyMsec;
    double                avgReplyMsec;
    long                  sendCount;
    long                  replyCount;
    long                  errorCount;
    int                   maxOidsPerReq;
    devSnmp_v3params      v3params;

    devSnmp_oid *findOID(char *oidStr);
    devSnmp_oid *createOID(configDataOid *base, OID *oid);
    devSnmp_pv *createPV(configDataPV *extra, devSnmp_oid *pOID, struct dbCommon *pRecord);
};
//----------------------------------------------------------------------

class devSnmp_host
// one of these exists for every SNMP remote host
{
  public:
    devSnmp_host(devSnmp_manager *pMgr, char *host, bool *okay);
    virtual ~devSnmp_host(void);
    char *hostName(void);
    devSnmp_pv *addPV(configDataOid   *base,
                      configDataPV    *extra,
                      OID             *oid,
                      struct dbCommon *pRecord);
    void processing(epicsTimeStamp *pnow);
    void zeroCounters(void);
    void report(int level, char *match);
    bool reportMatchAny(char *match);
    void queueGetTransaction(devSnmp_getTransaction *pTrans);
    void queueSetTransaction(devSnmp_setTransaction *pTrans);

    int getSnmpVersion(void);
    void setSnmpVersion(int version);
    void setSnmpV3Param(const char *param, const char *value, bool ignoreVersion=false);
    void setSnmpV3ConfigFile(const char *fileName);
    void getSnmpV3Params(devSnmp_v3params *params);

    int getMaxOidsPerReq(void);
    void setMaxOidsPerReq(int maxoids);

    void sessionRetriesChange(void);
    void sessionTimeoutChange(void);

  protected:
    devSnmp_manager *pOurMgr;
    char            *hostname;
    snmpPointerList *groupList;
    snmpPointerList *getQueue;
    snmpPointerList *setQueue;
    snmpPointerList *activeSessionList;
    int              snmpVersion;
    int              maxOidsPerReq;

    devSnmp_v3params v3params;

    devSnmp_group *findGroup(char *community);
    devSnmp_group *createGroup(char *community);
};
//----------------------------------------------------------------------
class devSnmp_manager
// object to manage other devSnmp_xxx objects
// devSnmp has one and only one of these
{
  public:
    devSnmp_manager(void);
    virtual ~devSnmp_manager(void);
    void setHostSnmpVersion(char *host, char *versionStr);
    void setHostSnmpV3Param(char *host, char *param, char *value);
    void setHostSnmpV3ConfigFile(char *host, char *fileName);
    int getHostSnmpVersion(char *host);
    void getHostSnmpV3Params(char *host, devSnmp_v3params *v3params);
    int getHostMaxOidsPerReq(char *host);
    void setMaxOidsPerReq(char *host, int maxoids);
    devSnmp_pv *addPV(struct dbCommon *pRec, struct link *pLink);
    void processing(epicsTimeStamp *pnow);
    void zeroCounters(void);
    void report(int level, char *match);
    bool reportMatchAny(char *match);

    void sessionRetriesChange(void);
    void sessionTimeoutChange(void);

    int start(void);
    int readTask(void);
    int sendTask(void);

    void sessionMutexLock(void);
    void sessionMutexUnlock(void);

    void incActiveRequests(void);
    void decActiveRequests(void);

  protected:
    snmpPointerList *snmpHostList;
    bool             started;
    epicsMutexId     sessionMutex;
    int              activeRequests;

    epicsThreadId    sendTask_id;
    snmpTimeObject   sendTask_start;
    unsigned long    sendTask_loops;
    bool             sendTask_abort;
    bool             sendTask_exited;

    epicsThreadId    readTask_id;
    snmpTimeObject   readTask_start;
    unsigned long    readTask_loops;
    int              readTask_stat;
    int              readTask_fds;
    int              readTask_block;
    fd_set           readTask_fdset;
    struct timeval   readTask_timeout;
    bool             readTask_abort;
    bool             readTask_exited;
    bool             readTask_inSelect;
    unsigned long    readTask_ignoreBlocks;

    devSnmp_host *findHost(char *host);
    devSnmp_host *createHost(char *host);

};
//----------------------------------------------------------------------
class snmpPollAggregate
// class to generate average poll times report for a number of devices
{
  public:
    snmpPollAggregate(void);
    virtual ~snmpPollAggregate(void);
    void addOID(devSnmp_oid *pOID);
    void report(void);

  protected:
    snmpPointerList *lists;

    snmpPointerList *findList(unsigned long msec);
};
//----------------------------------------------------------------------

extern "C" {
  // externally callable routines
  int epicsSnmpInit(int param);
  int devSnmpSetSnmpVersion(char *hostName, char *versionStr);
  int devSnmpSetSnmpV3Param(char *hostName, char *paramName, char *value);
  int devSnmpSetSnmpV3ConfigFile(char *hostName, char *fileName);
  int devSnmpSetMaxOidsPerReq(char *hostName, int maxoids);
  int devSnmpSetParam(const char *param, int value);
  int devSnmpSetDebug(int level);
  int snmpr(int level, char *match);
  int snmpz(void);
  int snmpzr(int level, char *match);
#if devSnmp_NETSNMP_VERSION < 50400
  void init_mib(void);
#else
  void netsnmp_init_mib(void);
#endif
}  // extern "C"

#endif  // DEVSNMP_H





