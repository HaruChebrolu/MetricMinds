from backend.connection import get_db_conn

# Tool Functions
def get_diskoccupation(*args, **kwargs):
    query_disk_occupation = """
        SELECT 
            labels->>'instance' AS instance, 
            SUM(value) AS total_disk_occupation 
        FROM ceph_cephdiskoccupation_metrics 
        GROUP BY instance;
        """    
    conn = get_db_conn()
    if not conn:
        return "❌ Database connection failed."  
    cursor = conn.cursor()
    try:     
        cursor.execute(query_disk_occupation)
        disk_occupation_results = cursor.fetchall()

        print("\n### Ceph Disk Occupation Per Node ###")
        for row in disk_occupation_results:
            print(f"Node: {row[0]}, Disk Occupation: {row[1]}")
        
        return disk_occupation_results
    except Exception as e:
        print("❌ Error getting disk occupation status:", e)
    finally:
        cursor.close()
        conn.close()


def check_degraded_pgs(*args, **kwargs):
    # Query to check if any degraded PGs exist
    query = """
    SELECT 
        CASE 
            WHEN MAX(value) > 0 THEN 'True'
            ELSE 'False'
        END AS degraded_pgs
    FROM ceph_cephpgdegraded_metrics;
    """
    conn = get_db_conn()
    if not conn:
        return "❌ Database connection failed."  
    cursor = conn.cursor()
    try:     
        
        cursor.execute(query)
        result = cursor.fetchone()[0]

        print(f"Degraded PGs: {result}")
        cursor.close()
        conn.close()
        return result
    
    except Exception as e:
        print("❌ Error checking degraded PGs:", e)
    finally:
        cursor.close()
        conn.close()
        
def check_recent_osd_crashes(*args, **kwargs):
    # Query to check if any failed OSDs exist
    query = """
        WITH osd_status AS (
        SELECT 
            labels->>'ceph_daemon' AS osd_id, 
            value, 
            timestamp,
            LAG(value) OVER (
                PARTITION BY labels->>'ceph_daemon' 
                ORDER BY timestamp ASC
            ) AS previous_value
        FROM ceph_cephosdup_metrics
        WHERE metric_name = 'ceph_osd_up'
    )
    SELECT osd_id, value AS current_status, previous_value, timestamp 
    FROM osd_status
    WHERE previous_value = 1.0 AND value = 0.0
    ORDER BY timestamp DESC;
    """

    conn = get_db_conn()
    if not conn:
        return "❌ Database connection failed."
    cursor = conn.cursor()

    try:        
        cursor.execute(query)
        crashed_osds = cursor.fetchall()

        if crashed_osds:
            response = "\n🚨 **YES!! AN OSD CRASH DETECTED!** 🚨\n"
            for osd in crashed_osds:
                osd_id, current_status, previous_value, timestamp = osd
                response += f"🛑 **OSD {osd_id} went DOWN at {timestamp}**\n"
            return response  # Return a formatted response with OSD crash details
        else:
            return "✅ No OSD failures detected."
        
    except Exception as e:
        return f"❌ Error executing query: {e}"
    finally:
        cursor.close()
        conn.close()
        
def get_cluster_health():
    query = "SELECT MAX(value) FROM ceph_health_status;"
    
    conn = get_db_conn()
    if not conn:
        return {"status": "error", "message": "❌ Database connection failed."}

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        
        if not result or result[0] is None:
            return {"status": "error", "message": "⚠️ No health data available."}

        health_status = int(result[0])

        health_messages = {
            0: "🟢 Cluster is healthy (HEALTH_OK)",
            1: "🟡 Cluster has warnings (HEALTH_WARN)",
            2: "🔴 Cluster has critical issues (HEALTH_ERR)"
        }

        return {"status": "success", "health": health_messages.get(health_status, "Unknown health status")}
    
    except Exception as e:
        return {"status": "error", "message": f"❌ Error fetching cluster health: {str(e)}"}
    
    finally:
        cursor.close()
        conn.close()


