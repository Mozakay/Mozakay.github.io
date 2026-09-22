---
layout: post
title: "Security Audit of a Docker-Based Cloud Application"
categories: ["Cloud Operations and Management"]
unit: 7
journey_group: "unit-7"
---

## 1. Scope and Architecture

This security audit assessed a Docker-based application deployed in Microsoft Azure as part of a cloud operations and management exercise. The environment consisted of two Ubuntu virtual machines. The first VM hosted the application workload and ran two Docker containers: an Nginx web server and a MongoDB database. Docker was verified as successfully installed and operational on the application host, as shown in Figure 1, while the deployed Nginx and MongoDB containers and their published ports are shown in Figure 2. The second VM hosted Greenbone Community Edition/OpenVAS and was used as an independent vulnerability-scanning node.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%201%20Docker%20successfully%20installed%20and%20running%20on%20the%20Azure%20Ubuntu%20VM..png" alt="Figure 1. Docker successfully installed and running on the Azure Ubuntu VM.">
  <figcaption><em>Figure 1: Docker successfully installed and running on the Azure Ubuntu VM.</em></figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%202%20Deployed%20Docker%20web%20and%20MongoDB%20containers%20with%20exposed%20ports%2080%20and%2027017..png" alt="Figure 2. Deployed Docker web and MongoDB containers with exposed ports 80 and 27017.">
  <figcaption><em>Figure 2: Deployed Docker web and MongoDB containers with exposed ports 80 and 27017.</em></figcaption>
</figure>

The architecture intentionally exposed selected services so that the security of both the application and its supporting cloud infrastructure could be assessed. Nginx was published through TCP port 80, MongoDB through TCP port 27017, and SSH administration through TCP port 22. Azure Network Security Group (NSG) rules initially allowed these services from unrestricted sources, as demonstrated in Figure 3. The Nginx service was also confirmed to be externally reachable through the cloud environment, as shown in Figure 4. This configuration created a realistic cloud-operations scenario because infrastructure risk is often introduced through configuration decisions rather than software vulnerabilities alone. Torkura et al. (2021) identify cloud misconfiguration, excessive permissions and unnecessarily exposed resources as important sources of cloud security risk.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%203%20Azure%20Network%20Security%20Group%20inbound%20rules%20allowing%20SSH%2C%20HTTP%20and%20MongoDB%20traffic..png" alt="Figure 3. Azure Network Security Group inbound rules allowing SSH, HTTP and MongoDB traffic.">
  <figcaption><em>Figure 3: Azure Network Security Group inbound rules allowing SSH, HTTP and MongoDB traffic.</em></figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%204%20Nginx%20web%20application%20successfully%20accessible%20through%20the%20Azure%20public%20endpoint..png" alt="Figure 4. Nginx web application successfully accessible through the Azure public endpoint.">
  <figcaption><em>Figure 4: Nginx web application successfully accessible through the Azure public endpoint.</em></figcaption>
</figure>

The audit scope therefore included the external network surface, Azure NSG configuration, Docker runtime settings, operating-system condition, SSH configuration, database access controls and vulnerabilities detected by OpenVAS. Container security was considered separately from conventional VM security because Docker introduces additional risks relating to runtime privileges, image content and host interaction (Martin et al., 2018).

## 2. OpenVAS Scanning Method and Configuration

The assessment combined automated vulnerability scanning with manual configuration inspection. This was necessary because a vulnerability scanner can identify remotely visible weaknesses, but it cannot fully evaluate cloud access rules, runtime privilege settings or authentication design. Kritikos et al. (2019) note that vulnerability-assessment tools differ in scope and coverage, supporting the use of complementary assessment methods.

Greenbone Community Edition was deployed on a separate Azure VM. Its core services were verified as operational before scanning, as shown in Figure 5. The management interface was then accessed through an SSH tunnel rather than being exposed directly to the Internet, as illustrated in Figure 6. This was preferable to exposing the scanner interface publicly and reflects good operational practice because the assessment platform itself should not unnecessarily increase the attack surface.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%205%20Key%20Greenbone%20Community%20Edition%20services%20running%20successfully%20on%20the%20Azure%20OpenVAS%20VM..png" alt="Figure 5. Key Greenbone Community Edition services running successfully on the Azure OpenVAS VM.">
  <figcaption><em>Figure 5: Key Greenbone Community Edition services running successfully on the Azure OpenVAS VM.</em></figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%206%20OpenVAS%20web%20interface%20successfully%20accessed%20through%20an%20SSH%20tunnel..png" alt="Figure 6. OpenVAS web interface successfully accessed through an SSH tunnel.">
  <figcaption><em>Figure 6: OpenVAS web interface successfully accessed through an SSH tunnel.</em></figcaption>
</figure>

A scan target representing the Docker application host was created in OpenVAS. The Full and fast scan configuration and All IANA assigned TCP port list were selected. The initial scan completed without identifying a host. Instead of treating this result as evidence that the system was secure, the scan configuration was reviewed. The target’s Alive Test was changed to Consider Hosts as Alive, after which the scan was repeated successfully.

The successful scan was then observed running against the Docker target, as shown in Figure 7, and it completed with an overall low-severity score of 2.6, as shown in Figure 8. The completed report confirmed that one host had been successfully assessed and that exposed ports, applications and security results had been identified, as shown in Figure 9.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%207%20OpenVAS%20Full%20and%20Fast%20scan%20running%20against%20the%20Docker%20audit%20target..png" alt="Figure 7. OpenVAS Full and Fast scan running against the Docker audit target.">
  <figcaption><em>Figure 7: OpenVAS Full and Fast scan running against the Docker audit target.</em></figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%208%20OpenVAS%20Full%20and%20Fast%20scan%20completed%20successfully%20with%20a%20Low%20severity%20score%20of%202.6..png" alt="Figure 8. OpenVAS Full and Fast scan completed successfully with a Low severity score of 2.6.">
  <figcaption><em>Figure 8: OpenVAS Full and Fast scan completed successfully with a Low severity score of 2.6.</em></figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%209%20OpenVAS%20report%20confirming%20one%20host%20scanned%20successfully%20with%20detected%20ports%2C%20applications%20and%20security%20results..png" alt="Figure 9. OpenVAS report confirming one host scanned successfully with detected ports, applications and security results.">
  <figcaption><em>Figure 9: OpenVAS report confirming one host scanned successfully with detected ports, applications and security results.</em></figcaption>
</figure>

This step was operationally important because it demonstrated that scanner output requires interpretation. A “no findings” result may reflect discovery or configuration problems rather than an absence of vulnerabilities. The successful scan identified one host, five application signatures and two reportable low-severity findings.

Manual inspection was then used to examine published Docker ports, privileged mode, configured container users and MongoDB authentication behaviour. This additional review was important because container security depends on runtime and deployment configuration as well as known software vulnerabilities (Martin et al., 2018; Fernández González et al., 2022).

## 3. Findings and Critical Analysis

OpenVAS identified two low-severity vulnerabilities, both with a severity score of 2.6. The detailed scan results are shown in Figure 10.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%2010%20OpenVAS%20scan%20results%20identifying%20low-severity%20SSH%20and%20TCP%20information%20disclosure%20findings%20on%20the%20Docker%20audit%20host..png" alt="Figure 10. OpenVAS scan results identifying low-severity SSH and TCP information disclosure findings on the Docker audit host.">
  <figcaption><em>Figure 10: OpenVAS scan results identifying low-severity SSH and TCP information disclosure findings on the Docker audit host.</em></figcaption>
</figure>

The first was Weak MAC Algorithm(s) Supported (SSH). The SSH service supported two 64-bit UMAC algorithms. Although the finding did not indicate immediate system compromise, weaker cryptographic algorithms provide unnecessary exposure and should be removed when stronger alternatives are available. The low scanner score should therefore not be interpreted as a reason to ignore the issue.

The second finding was TCP Timestamps Information Disclosure. The host implemented TCP timestamps under RFC1323/RFC7323, which may allow an external observer to estimate system uptime. The direct impact is limited; however, uptime and host characteristics can support reconnaissance. This illustrates the difference between direct exploitability and information value: a low-severity weakness can still contribute to a broader attack sequence.

The manual cloud configuration review revealed risks that were more operationally significant than the two OpenVAS findings. MongoDB was bound to 0.0.0.0:27017, while the Azure NSG permitted traffic to TCP/27017 from unrestricted sources. The Docker-side exposure of Nginx and MongoDB is shown in Figure 11, while the corresponding unrestricted NSG rules are shown in Figure 3. These controls operate at different layers but combine to create an unnecessary exposure path: Docker makes the service available on the host network interfaces, while the NSG permits external traffic to reach that port. This supports Torkura et al.’s (2021) argument that cloud risk frequently arises from configuration state and exposure.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%2011%20Docker%20containers%20showing%20Nginx%20and%20MongoDB%20services%20exposed%20on%20host%20ports%2080%20and%2027017..png" alt="Figure 11. Docker containers showing Nginx and MongoDB services exposed on host ports 80 and 27017.">
  <figcaption><em>Figure 11: Docker containers showing Nginx and MongoDB services exposed on host ports 80 and 27017.</em></figcaption>
</figure>

MongoDB authentication also required further hardening. The observed container command was mongod, and a connection-status check returned no authenticated users or roles, as shown in Figure 12. This evidence does not prove that unauthenticated external users could read or modify data because no external data-access test was performed. However, explicit authentication enforcement was not demonstrated in the inspected runtime configuration. The issue is therefore best classified as an authentication-assurance and configuration concern rather than evidence of compromise. Fernández González et al. (2022) similarly emphasise secure configuration as part of container hardening.

<figure>
  <img src="https://raw.githubusercontent.com/Mozakay/Mozakay.github.io/main/assets/images/COM/unit7/part1/Figure%2012%20MongoDB%20configuration%20and%20connection%20status%20showing%20successful%20access%20with%20no%20authenticated%20users%20or%20roles..png" alt="Figure 12. MongoDB configuration and connection status showing successful access with no authenticated users or roles.">
  <figcaption><em>Figure 12: MongoDB configuration and connection status showing successful access with no authenticated users or roles.</em></figcaption>
</figure>

SSH was also reachable from unrestricted network sources, as shown in Figure 3. Key-based authentication was used, which is a positive control, but broad exposure still increases the number of automated scanning and exploitation attempts that the service must withstand. Nginx was accessible through HTTP rather than HTTPS, and its public accessibility over HTTP was demonstrated in Figure 4, meaning transport encryption was not provided.

The Docker inspection identified a positive control: both containers returned privileged=false. This reduces the ability of a compromised container to obtain extensive host privileges. However, no explicit container user was configured. This does not prove that the containers were running as root, but least-privilege execution was not explicitly demonstrated and should therefore be verified.

The Ubuntu host also reported pending updates and required a restart. From a cloud-operations perspective, this is important because vulnerability management is not completed when a weakness is detected; patching, rebooting and verification are also operational responsibilities. Dissanayake et al. (2022) describe security patch management as essential but operationally complex, reinforcing the need for a controlled update and validation process.

## 4. ISO/IEC 27001:2022 Alignment

The identified risks and proposed remediation controls were mapped to relevant ISO/IEC 27001:2022 Annex A controls.

The OpenVAS findings shown in Figure 10, together with the pending operating-system updates identified during the host review, relate to A.8.8 Management of technical vulnerabilities, because they concern the identification, assessment and treatment of known technical weaknesses. The recommendation to patch the host and repeat the vulnerability scan directly supports this control.

The Docker configuration findings align with A.8.9 Configuration management. This includes the exposed MongoDB service shown in Figure 11, the absence of an explicitly configured container user and the need to verify secure runtime settings. Secure container configuration is therefore part of the wider operational requirement to maintain controlled and hardened cloud infrastructure.

The unrestricted SSH and MongoDB network rules shown in Figure 3 align with A.8.20 Network security, A.8.21 Security of network services and A.8.22 Segregation of networks. Restricting TCP/22 and TCP/27017 to authorised or private network paths would reduce unnecessary exposure and provide stronger separation between administrative, application and database services.

The SSH MAC weakness identified in Figure 10 and the use of unencrypted HTTP demonstrated in Figure 4 align with A.8.24 Use of cryptography. Disabling weak SSH MAC algorithms and replacing HTTP with HTTPS would strengthen cryptographic protection for management and application traffic.

The MongoDB authentication concern evidenced in Figure 12 aligns with A.5.15 Access control and A.8.5 Secure authentication. Explicitly enabling authentication, applying least-privilege accounts and protecting credentials would improve access control and authentication assurance.

The audit also supports A.5.9 Inventory of information and other associated assets, because the assessment identified the cloud host, operating system, containerised services and externally exposed network services through the architecture review and OpenVAS scan results shown in Figures 2, 9 and 11. Accurate asset identification is necessary for effective monitoring, vulnerability management and change control.

Logging was not assessed in sufficient depth to demonstrate alignment with A.8.15 Logging. Therefore, centralised collection and review of Azure activity logs, operating-system logs, Docker logs and application logs are recommended as future operational controls.

Overall, the ISO/IEC 27001 mapping shows that the remediation actions are not isolated technical fixes; they support a broader cloud security management approach covering vulnerability management, secure configuration, access control, network protection, cryptography, asset management and logging. This is particularly relevant to cloud operations and management, where security depends on maintaining the configuration and operational state of multiple interconnected services.

## 5. Limitations and Future Improvements

This was a point-in-time security audit rather than a complete penetration test. OpenVAS provided useful external vulnerability information, but scanner coverage varies between tools and detection methods (Kritikos et al., 2019).

The Docker assessment was also selective. It examined exposed ports, privileged mode, configured users and MongoDB authentication behaviour, supported by the configuration evidence in Figures 11 and 12, but it did not perform a complete CIS Docker Benchmark assessment.

The audit did not systematically test HTTP security headers, container-image provenance, base-image vulnerabilities, secret-management practices or Docker network segmentation. Although image versions were identified, no dedicated image scanner such as Trivy or Grype was used to determine whether the images or base layers contained known CVEs. Secret storage and handling were also not examined in enough depth to make conclusions about secret-management quality.

Centralised logging and log-review practices were not examined in detail, so alignment with ISO/IEC 27001 control A.8.15 could not be validated.

The MongoDB assessment demonstrated a session without an authenticated identity, as shown in Figure 12, but external unauthorised data access was not attempted. The evidence therefore supports incomplete authentication assurance rather than a claim that the database was remotely compromised.

Future work should include container-image scanning, HTTP security-header testing, secret-management review, Docker network-segmentation assessment and centralised logging. Continuous auditing would also improve assurance because later changes to NSGs, containers, images or packages can alter the security posture after a point-in-time assessment (Torkura et al., 2021).

## 6. Recommendations and Conclusion

Risk treatment should prioritise controls that reduce exposure before lower-impact hardening issues. The first priority is therefore to remove unnecessary public database exposure. The unrestricted MongoDB rule demonstrated in Figure 3 should be removed, and TCP/27017 should be restricted to private application communication. MongoDB authentication should be explicitly enabled and verified, with least-privilege accounts and protected credentials.

Administrative SSH access should be limited to authorised addresses, VPN access or Azure Bastion. The weak SSH MAC algorithms identified by OpenVAS in Figure 10 should be disabled. Nginx should move from HTTP to HTTPS using TLS, with HTTP redirected to port 443.

Pending operating-system updates should be tested and applied, followed by the required restart and a repeat vulnerability scan. Dissanayake et al. (2022) show that patch management should be treated as an ongoing process involving identification, prioritisation, deployment and verification.

Docker containers should continue to operate without privileged mode, while explicit non-root execution should be configured where supported. Secure container operation depends on runtime settings as well as image contents (Martin et al., 2018; Fernández González et al., 2022).

Overall, OpenVAS identified only two low-severity vulnerabilities, as shown in Figures 8 and 10, but the manual cloud and Docker review identified additional risks related to network exposure, authentication assurance, encryption and patch management. This is an important cloud-operations finding: a low vulnerability-scanner score does not automatically mean that the overall deployment has a low security risk.

The exercise demonstrated that an effective cloud security audit requires both automated vulnerability assessment and configuration-level operational review. Combining these approaches produced a clearer view of the deployment and resulted in practical remediation actions that can be implemented and verified through a subsequent scan.

## References

Dissanayake, N., Jayatilaka, A., Zahedi, M. and Babar, M.A. (2022) ‘Software security patch management – A systematic literature review of challenges, approaches, tools and practices’, Information and Software Technology, 144, 106771. Available at: .

Fernández González, D., Rodríguez Lera, F.J., Esteban, G. and Fernández Llamas, C. (2022) ‘SecDocker: Hardening the Continuous Integration Workflow’, SN Computer Science, 3, 80. Available at: .

International Organization for Standardization (ISO) (2022) ISO/IEC 27001:2022 Information security, cybersecurity and privacy protection — Information security management systems — Requirements. Geneva: ISO.

Kritikos, K., Magoutis, K., Papoutsakis, M. and Ioannidis, S. (2019) ‘A survey on vulnerability assessment tools and databases for cloud-based web applications’, Array, 3–4, 100011. Available at: .

Martin, A., Raponi, S., Combe, T. and Di Pietro, R. (2018) ‘Docker ecosystem – Vulnerability analysis’, Computer Communications, 122, pp. 30–43. Available at: .

Torkura, K.A., Sukmana, M.I.H., Cheng, F. and Meinel, C. (2021) ‘Continuous auditing and threat detection in multi-cloud infrastructure’, Computers & Security, 102, 102124. Available at: .
