---
layout: post
title: "Unit 8: Disaster Recovery Plan for a Cloud-Based Infrastructure on Microsoft Azure"
categories: ["Cloud Operations and Management"]
unit: 8
journey_group: "unit-8"
---

## Context and Purpose

### Introduction

Cloud infrastructure can be disrupted by accidental deletion, database corruption, ransomware-style file loss and service failure. Disaster Recovery (DR) therefore requires more than storing a copy of data; it requires a defined recovery process, measurable recovery objectives and testing to confirm that the protected system can be returned to an operational state. Swanson et al. (2010) emphasise that contingency planning should define recovery requirements, implement appropriate recovery strategies and validate them through practical testing.

For this project, a DR environment was built on Microsoft Azure using Restic 0.18.1 as the backup and recovery tool. The test simulated destructive file loss together with deletion of a PostgreSQL database table. Recovery effectiveness was evaluated using Recovery Time Objective (RTO) and Recovery Point Objective (RPO), which are commonly used to evaluate disaster recovery solutions (Mendonça, Lima and Andrade, 2020).

## Implementation and Evidence

### Azure Architecture and Backup Strategy

Figure 1 presents the logical DR architecture. The protected workload was deployed on an Ubuntu Server 24.04 LTS Azure Virtual Machine named vm-dr-app in the Austria East region. The VM contained the application data under /srv/cloudapp, the PostgreSQL database drdb, and the Restic client. Network access was provided through an Azure Public IP and controlled using the Network Security Group vm-dr-app-nsg, with SSH used for controlled administration. The implemented Azure resources are confirmed by the Azure Resource Visualizer in Figure 2.

<img src="{{ '/assets/images/COM/unit8/pic%201.png' | relative_url }}" alt="Figure 1: DR Architecture Design" width="500">

*Figure 1: DR Architecture Design*

<img src="{{ '/assets/images/COM/unit8/Pic%202.png' | relative_url }}" alt="Figure 2: Actual Azure Deployment" width="500">

*Figure 2: Actual Azure Deployment*

The backup destination was separated from the VM. Restic stored encrypted snapshots in the restic-backup Blob Container within the Azure Storage Account mozadrbackup01, hosted in Qatar Central. This separation is important because a destructive event affecting the VM does not automatically remove the historical backup copies stored in the remote repository. Microsoft (2026a) recommends considering backup, recovery and failover when designing resilient Azure storage solutions, while Microsoft (2026b) explains that Azure redundancy protects against certain infrastructure failures. However, redundancy alone is not equivalent to historical backup because unwanted deletion or corruption can also affect replicated data.

The protected content consisted of application files and a PostgreSQL database dump (drdb.sql). Three Restic snapshots were created during the test. Figure 3 shows snapshots at 05:59:08, 06:00:20 and 06:01:21 UTC, with the final snapshot containing approximately 24.416 MiB. After the final valid snapshot, six additional application files and 180 database orders were deliberately created without taking another backup. The database therefore increased from 252,700 protected orders to 252,880 orders.

For the production design, an hourly backup interval is proposed, giving a target RPO of 60 minutes. Daily, weekly or monthly retention could also be applied depending on organisational requirements. In this implementation, the snapshots were triggered manually within an accelerated test period; therefore, the experiment validates the recovery process rather than an automated hourly schedule.

<img src="{{ '/assets/images/COM/unit8/pic3.png' | relative_url }}" alt="Figure 3: Backup state and post-backup data before failure" width="500">

*Figure 3: Backup state and post-backup data before failure*

### Failure Scenario

A ransomware-style destructive data-loss scenario was simulated. At 06:02:30 UTC, the application files under /srv/cloudapp were deleted, reducing the application file count to zero. At the same time, the PostgreSQL orders table was deliberately dropped. Figure 4 confirms both conditions: the application files were removed and a subsequent database query returned “relation ‘orders’ does not exist.”

The test was designed to represent a realistic data-loss incident, where both application files and database data become unavailable at the same time. Yun et al. (2017) highlight the importance of recoverable historical copies in ransomware scenarios because recovery requires returning data to a known-good state rather than simply restoring system availability.

<img src="{{ '/assets/images/COM/unit8/pic4.png' | relative_url }}" alt="Figure 4: Failure simulation" width="500">

*Figure 4: Failure simulation*

### Recovery Process Using Restic

Recovery began at 06:04:30 UTC. Restic first identified the latest valid snapshot, which had been created at 06:01:21 UTC. The command restic restore latest restored the protected data into a temporary recovery location before the application files were copied back to /srv/cloudapp.

Figure 5 records the recovery operation. Restic restored 1,475 files/directories representing 24.416 MiB, while the application-level file count returned to 1,471 files. The PostgreSQL dump contained in the restored snapshot was then used to reconstruct the database. Figure 6 confirms that the orders table was successfully restored with exactly 252,700 records. Recovery was completed at 06:06:19 UTC.

<img src="{{ '/assets/images/COM/unit8/pic5.png' | relative_url }}" alt="Figure 5: Recovery from latest Restic snapshot" width="500">

*Figure 5: Recovery from latest Restic snapshot*

<img src="{{ '/assets/images/COM/unit8/pic6.png' | relative_url }}" alt="Figure 6: Database restored to 252,700" width="500">

*Figure 6: Database restored to 252,700*

Finally, restic check was executed to verify repository integrity. Figure 7 shows that all three snapshots were checked successfully and that “no errors were found.” This final check confirmed that the repository was still healthy after the recovery test.

<img src="{{ '/assets/images/COM/unit8/pic7.png' | relative_url }}" alt="Figure 7: Repository integrity check" width="500">

*Figure 7: Repository integrity check*

## Technical Analysis

### RTO and RPO Evaluation

Recovery Time Objective (RTO) is the maximum acceptable period within which a disrupted service should be restored. Recovery Point Objective (RPO) is the maximum acceptable data loss expressed as the time between the latest recoverable backup and the disruptive event (Mendonça, Lima and Andrade, 2020). Table 1 compares the planned targets with the measured Azure test results.

**Table 1: Disaster Recovery Test Results**

| Measure | Target / Expected State | Actual Azure Test Result | Evaluation |
|---|---|---|---|
| RTO | ≤ 30 minutes | 3 min 49 sec (229 sec) | Met |
| Proposed production RPO | ≤ 60 minutes | Hourly backup strategy proposed | Supported by design |
| Observed snapshot-to-incident gap | Test measurement | 1 min 9 sec (69 sec) | Within target |
| Latest valid snapshot | Known-good recovery point | 06:01:21 UTC | Confirmed |
| Incident time | Recorded failure event | 06:02:30 UTC | Confirmed |
| Recovery started | Recorded | 06:04:30 UTC | Confirmed |
| Recovery completed | Service/data restored | 06:06:19 UTC | Confirmed |
| Orders before incident | 252,880 | 252,880 | Confirmed |
| Orders in final valid backup | 252,700 | 252,700 restored | Pass |
| Post-backup orders | 180 expected unrecoverable | 180 lost | Expected |
| Post-backup files | 6 expected unrecoverable | 6 lost | Expected |
| Protected application files | Restore latest valid state | 1,471 restored | Pass |
| Restic restore | Successful restoration | 1,475 files/directories; 24.416 MiB | Pass |
| Repository integrity | No repository errors | No errors found | Pass |

The RTO target was 30 minutes. The incident began at 06:02:30 UTC and recovery was completed at 06:06:19 UTC, giving an actual RTO of 3 minutes 49 seconds (229 seconds). The recovery therefore met the RTO by a substantial margin. The proposed production RPO was 60 minutes, based on an intended hourly backup policy. During the accelerated Azure test, the final valid snapshot was created at 06:01:21 UTC and the incident occurred at 06:02:30 UTC, producing an observed recovery-point gap of 69 seconds. This result is within the 60-minute objective, although it should be interpreted as a test observation rather than proof of automated hourly scheduling.

The data difference demonstrates the practical impact of RPO. Immediately before the incident, the database contained 252,880 orders, while the latest protected snapshot contained 252,700. Consequently, 180 post-backup orders were not recoverable. The six files created after the final snapshot were also lost. These losses were expected because Restic can only restore data captured in a valid snapshot. The result shows why shorter backup intervals reduce potential data loss, while more frequent backups also increase storage activity and operational overhead.

## Conclusion

The project successfully designed and implemented a functional DR solution on Microsoft Azure using Restic and Azure Blob Storage. The test demonstrated recovery from destructive application-file loss and PostgreSQL table deletion using the latest valid Restic snapshot. The database was restored to 252,700 records, application files were recovered, and repository validation reported no errors.

The measured RTO of 3 minutes 49 seconds met the 30-minute objective. The observed recovery-point gap of 69 seconds was within the proposed 60-minute RPO, while the loss of 180 orders and six post-backup files demonstrated the direct relationship between backup frequency and recoverable data. The results therefore show that the implemented architecture provides an effective recovery mechanism, although automated hourly scheduling would be required in production to consistently enforce the proposed one-hour RPO.

## Critical Reflection

Thank you for your continued guidance and support. Your feedback has helped me improve the way I present and structure my response more clearly and accurately.

I would like to clarify that the 69-second value recorded in the test was the observed gap between the final valid snapshot at 06:01:21 UTC and the simulated failure at 06:02:30 UTC. It was therefore an observed recovery-point gap, not the RPO itself. The defined production RPO target remained 60 minutes, based on the proposed hourly backup strategy.

The implemented DR solution successfully validated backup and recovery on Azure; however, the backup schedule was manually triggered during the exercise. To make the implemented solution operational on a continuous basis, the proposed hourly backup schedule should be automated and monitored so that missed or failed backup jobs are detected and the 60-minute RPO target is maintained consistently. Microsoft Azure Backup provides monitoring of backup jobs and health, together with Azure Monitor alerts for backup and restore failures, which would strengthen the reliability of the implemented DR process (Microsoft, 2026c).

I reviewed the figures and the RTO/RPO table, and the overall numbering, captions and table structure are consistent. The explanation above clarifies the difference between the 60-minute RPO target and the 69-second observed recovery-point gap.

## References

Mendonça, J., Lima, R. and Andrade, E. (2020) ‘Evaluating and modelling solutions for disaster recovery’, International Journal of Grid and Utility Computing, 11(5), pp. 683–704. DOI: 10.1504/IJGUC.2020.110055.

Microsoft (2026a) Azure storage disaster recovery planning and failover. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/storage/common/storage-disaster-recovery-guidance (Accessed: 19 September 2026).

Microsoft (2026b) Azure Storage redundancy. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy (Accessed: 19 September 2026).

Microsoft (2026c) Monitoring and reporting solutions for Azure Backup. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/backup/monitoring-and-alerts-overview (Accessed: 19 September 2026).

Swanson, M., Bowen, P., Phillips, A.W., Gallup, D. and Lynes, D. (2010) Contingency Planning Guide for Federal Information Systems. NIST SP 800-34 Rev. 1.

Yun, J., Hur, J., Shin, Y. and Koo, D. (2017) ‘CLDSafe: An efficient file backup system in cloud storage against ransomware’, IEICE Transactions on Information and Systems, E100-D(9), pp. 2228



