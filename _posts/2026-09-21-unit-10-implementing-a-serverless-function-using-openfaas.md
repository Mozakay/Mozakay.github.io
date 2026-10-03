---
layout: post
title: "Unit 10: Implementing a Serverless Function Using OpenFaaS"
categories: ["Cloud Operations and Management"]
unit: 10
journey_group: "unit-10"
---

## Context and Purpose

Serverless computing enables developers to execute application logic without directly managing the underlying servers. In a Function-as-a-Service (FaaS) model, infrastructure responsibilities such as execution, scaling and resource allocation are largely handled by the platform, allowing developers to focus on individual application functions (Baldini et al., 2017; Leitner et al., 2019). In this implementation, a Python-based greeting function was developed and deployed using OpenFaaS on Kubernetes.

## Implementation and Evidence

### Kubernetes Environment

The deployment began by confirming that the Kubernetes environment was operational. Figure 1 shows the cluster nodes in the Ready state, confirming that Kubernetes was available to host the OpenFaaS workload.

<img src="{{ '/assets/images/COM/unit10/pic%201.png' | relative_url }}" alt="Figure 1. Kubernetes nodes in Ready state." width="700">

*Figure 1. Kubernetes nodes in Ready state.*

### OpenFaaS Platform Deployment

OpenFaaS was then installed on the Kubernetes cluster. Figure 2 confirms that the main OpenFaaS components, including the gateway, Prometheus, NATS and queue worker, were successfully running. The gateway provides the entry point for function requests, while Kubernetes manages the underlying containerised workloads (OpenFaaS, 2024a).

<img src="{{ '/assets/images/COM/unit10/pic%202.png' | relative_url }}" alt="Figure 2. OpenFaaS components running successfully." width="700">

*Figure 2. OpenFaaS components running successfully.*

### Python Greeting Function

The greeting function was created using the OpenFaaS Python HTTP template. Figure 3 presents the final Python function, which accepts a user name and returns a personalised greeting.

<img src="{{ '/assets/images/COM/unit10/pic%203.png' | relative_url }}" alt="Figure 3. Python greeting function." width="700">

*Figure 3. Python greeting function.*

### Deployment Configuration

The deployment configuration is shown in Figure 4. The stack.yaml file specifies the OpenFaaS gateway, Python runtime, handler location and container image required to build and deploy the function (OpenFaaS, 2024b).

<img src="{{ '/assets/images/COM/unit10/pic%204.png' | relative_url }}" alt="Figure 4. OpenFaaS stack configuration." width="700">

*Figure 4. OpenFaaS stack configuration.*

### Build and Deployment

The function was subsequently built into a container image, pushed to a registry and deployed through the OpenFaaS CLI. Figure 5 shows the successful deployment response, including 202 Accepted and the function endpoint.

<img src="{{ '/assets/images/COM/unit10/pic%205.png' | relative_url }}" alt="Figure 5. Successful OpenFaaS deployment." width="700">

*Figure 5. Successful OpenFaaS deployment.*

### Function Invocation

Finally, the function was invoked through the OpenFaaS CLI. As shown in Figure 6, the input Moza returned the expected greeting, confirming successful end-to-end execution.

<img src="{{ '/assets/images/COM/unit10/pic%206.png' | relative_url }}" alt="Figure 6. Successful invocation of the greeting function." width="700">

*Figure 6. Successful invocation of the greeting function.*

## Technical Discussion and Evaluation

From an operational perspective, serverless computing can improve cloud operations by reducing direct infrastructure management, supporting independent deployment and enabling functions to scale according to workload. Research also identifies improved resource utilisation and reduced operational overhead as important advantages of serverless architectures (Shafiei, Khonsari and Mousavi, 2022). OpenFaaS further separates application logic from the underlying Kubernetes infrastructure, allowing functions to be accessed through a standard gateway rather than individual pods.

However, serverless platforms can introduce challenges such as cold-start latency, monitoring complexity and additional platform dependencies (Baldini et al., 2017; Shafiei, Khonsari and Mousavi, 2022). Overall, the implementation demonstrated that OpenFaaS provides a practical approach to deploying lightweight and independently managed cloud functions.

## References

Baldini, I., Castro, P., Chang, K., Cheng, P., Fink, S., Ishakian, V., Mitchell, N., Muthusamy, V., Rabbah, R., Slominski, A. and Suter, P. (2017) ‘Serverless Computing: Current Trends and Open Problems’, in *Research Advances in Cloud Computing*. Singapore: Springer, pp. 1–20. doi: 10.1007/978-981-10-5026-8_1.

Leitner, P., Wittern, E., Spillner, J. and Hummer, W. (2019) ‘A mixed-method empirical study of Function-as-a-Service software development in industrial practice’, *Journal of Systems and Software*, 149, pp. 340–359. doi: 10.1016/j.jss.2018.12.013.

Shafiei, H., Khonsari, A. and Mousavi, P. (2022) ‘Serverless Computing: A Survey of Opportunities, Challenges, and Applications’, *ACM Computing Surveys*, 54(11s), Article 239, pp. 1–32. doi: 10.1145/3510611.

OpenFaaS (2024a) *OpenFaaS Stack*. Available at: https://docs.openfaas.com/architecture/stack/ (Accessed: 18 September 2026).

OpenFaaS (2024b) *OpenFaaS YAML Reference*. Available at: https://docs.openfaas.com/reference/yaml/ (Accessed: 18 September 2026).
