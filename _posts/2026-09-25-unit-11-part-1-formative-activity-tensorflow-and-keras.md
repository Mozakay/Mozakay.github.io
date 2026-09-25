---
layout: post
title: "Unit 11: Formative Activity: TensorFlow and Keras"
categories: ["Cloud Operations and Management"]
unit: 11
journey_group: "unit-11-part-1"
---

## Introduction

This activity implemented a convolutional neural network (CNN) for image recognition using TensorFlow and Keras in Google Colab, before packaging the trained model as a containerised API and deploying it to Microsoft Azure. The implementation therefore covered the principal stages of an AI application lifecycle: dataset preparation, model training, evaluation, containerisation, cloud deployment and remote inference. Nevertheless, successful deployment alone does not establish that a model is sufficiently accurate, efficient, scalable or robust for production use. The results must therefore be interpreted in relation to both predictive performance and operational limitations.

## Model Development and Dataset Preparation

Figure 1 confirms that TensorFlow 2.20.0 was successfully configured and that the CIFAR-10 dataset was loaded with 50,000 training and 10,000 test images. CIFAR-10 contains 60,000 colour images of 32 × 32 pixels distributed across ten mutually exclusive classes, making it suitable for a controlled image-classification experiment (Krizhevsky, 2009). TensorFlow was appropriate because it supports machine-learning computation across heterogeneous computing environments and was designed for large-scale training and inference workloads (Abadi et al., 2016). However, CIFAR-10 remains a relatively small and highly standardised benchmark. Consequently, performance on this dataset cannot be assumed to generalise directly to higher-resolution, imbalanced or operational image data.

![Figure 1. TensorFlow environment and CIFAR-10 dataset successfully loaded.](/assets/images/COM/unit11/part1/figure-1-tensorflow-cifar10.png)

*Figure 1. TensorFlow environment and CIFAR-10 dataset successfully loaded.*

## Training and Validation

Figure 2 demonstrates that the CNN learned progressively across ten epochs. Training accuracy increased from **40.73% to 80.47%**, while validation accuracy increased from **55.36% to 76.78%**. At the final epoch, training loss was **0.5512**, whereas validation loss was **0.6897**. The final difference of approximately **3.69 percentage points** between training and validation accuracy indicates a modest generalisation gap. The result is consistent with the established ability of CNNs to learn hierarchical representations that are effective for image classification (Rawat and Wang, 2017).

However, validation accuracy increased more slowly during the later epochs, rising only from **74.90% at epoch six to 76.78% at epoch ten**. This pattern suggests diminishing gains under the existing training configuration, although longer training was not tested and therefore cannot be ruled out as potentially beneficial. Higher training accuracy should not itself be interpreted as improved generalisation. Data augmentation, regularisation, dropout, learning-rate scheduling or architectural refinement could potentially improve performance on unseen data. Such improvements would nevertheless need to be balanced against computational and memory requirements, since efficient deep-learning design involves trade-offs between predictive performance, throughput, resource consumption and computational complexity (Sze et al., 2017).

![Figure 2. CNN model training and validation performance over 10 epochs.](/assets/images/COM/unit11/part1/figure-2-cnn-training-validation.png)

*Figure 2. CNN model training and validation performance over 10 epochs.*

## Model Evaluation

Figure 3 provides a stronger assessment of generalisation by evaluating the model against the held-out CIFAR-10 test set. The final test accuracy was **75.89%**, only **0.89 percentage points** below the final validation accuracy of 76.78%. This close correspondence suggests that validation performance transferred reasonably consistently to the test data. The selected test image was also correctly classified as a **cat**, with a reported confidence score of **79.62%**.

Nevertheless, neither the overall accuracy nor one successful example is sufficient to demonstrate comprehensive model reliability. Although CIFAR-10 is balanced across its ten classes, aggregate accuracy can still conceal class-specific weaknesses. A stronger evaluation would therefore include a confusion matrix, per-class precision and recall, repeated experiments using controlled random seeds and analysis of incorrectly classified images. Furthermore, the reported 79.62% confidence should not automatically be interpreted as a calibrated probability of correctness. Confidence calibration would need to be evaluated separately before such scores could be relied upon for risk-sensitive decisions.

![Figure 3. Final model test accuracy and sample image prediction.](/assets/images/COM/unit11/part1/figure-3-test-accuracy-prediction.png)

*Figure 3. Final model test accuracy and sample image prediction.*

## Containerisation and Azure Deployment

The deployment stage evaluated whether the trained model could operate successfully outside the development notebook. The model and API dependencies were packaged as a Docker container and uploaded to Azure Container Registry before deployment through Azure Container Apps. Containerisation was used to encapsulate the application and its dependencies within a consistent deployment unit, supporting the portability of the application across computing environments (Bernstein, 2014).

Importantly, the initial deployment did not succeed. Azure reported an unsupported image-layer MIME/compression format while attempting to provision the original container image. The image was subsequently rebuilt using Docker Buildx and pushed as a new version using OCI-compatible media types, after which the Azure Container App reached a **Succeeded** provisioning state. This troubleshooting process is significant because it demonstrates that reproducibility in cloud-based AI systems depends on more than the trained model itself. Container formats, runtime compatibility, registry configuration and deployment-platform requirements can all determine whether an otherwise functioning model can be operationalised successfully.

## Operational Validation and Production Readiness

The deployed application was then tested operationally. A request to the `/health` endpoint returned `{"status":"healthy"}`, confirming that the service was running and responding. Figure 4 records the subsequent live inference test against the deployed `/predict` endpoint. The remote Azure deployment classified the uploaded test image as **cat with 79.62% reported confidence**, matching the local prediction shown in Figure 3. This provides practical evidence that model serialisation, containerisation and cloud deployment preserved the inference behaviour of the trained model.

![Figure 4. Successful image prediction using the deployed CIFAR-10 model on Azure Container Apps.](/assets/images/COM/unit11/part1/figure-4-azure-container-apps-prediction.png)

*Figure 4. Successful image prediction using the deployed CIFAR-10 model on Azure Container Apps.*

However, functional equivalence between local and cloud inference is only a limited measure of production readiness. No systematic measurements were conducted for response latency, cold-start behaviour, concurrent requests, throughput, resource consumption or service availability. Security controls, authentication and monitoring were also outside the scope of this experiment. Therefore, the successful inference result demonstrates technical deployment viability rather than full operational readiness.

## Reflection on AI for Cloud Resource Management and Optimisation

The activity also illustrates the reciprocal relationship between artificial intelligence and cloud computing. Cloud platforms provide elastic computational resources for training and serving AI models, while AI techniques can in turn support more adaptive management of cloud resources. Auto-scaling must determine how much infrastructure should be allocated to changing workloads while balancing service-level requirements and cost. Lorido-Botran, Miguel-Alonso and Lozano (2014) identify this as a central challenge in elastic cloud environments and review approaches including threshold-based mechanisms, control theory, reinforcement learning, queuing theory and time-series techniques.

Machine-learning approaches could extend conventional scaling by using historical CPU utilisation, memory consumption, request volume and latency to forecast changes in workload before resource saturation occurs. Such predictive allocation could reduce unnecessary over-provisioning while potentially improving responsiveness. Nevertheless, prediction errors could also lead to under-provisioning, degraded service quality or unnecessary expenditure. Consequently, AI-based resource optimisation should be assessed against conventional reactive auto-scaling rather than assumed to be superior.

More advanced resource-management problems can also be formulated as learning tasks. Mao et al. (2016) demonstrated this through DeepRM, in which deep reinforcement learning was applied to multi-resource task scheduling. Their results showed that learned resource-management policies could perform comparably with established heuristics and adapt to different workload conditions. However, this does not imply that deep reinforcement learning is automatically appropriate for every cloud workload. Learned policies require representative training experience, suitable reward functions and continuing monitoring. A poorly designed optimisation objective could, for example, minimise infrastructure cost while unintentionally increasing response latency or reducing availability.

A more defensible operational approach would therefore combine AI-based forecasting or scheduling with explicit resource limits, service-level objectives, monitoring and conventional fail-safe scaling rules. AI should function as an optimisation mechanism within cloud governance rather than as an uncontrolled replacement for deterministic operational controls.

## Conclusion

Overall, the implementation successfully demonstrated a complete AI-to-cloud workflow. The **75.89% test accuracy** shows that the CNN learned a meaningful classification function, while the successful Azure deployment demonstrates that the trained model could be operationalised as a remotely accessible inference service. However, the results should be treated as a technically successful experimental baseline rather than evidence of production readiness. Future work should evaluate class-level performance, confidence calibration, inference latency, scalability, resource consumption and the effectiveness of AI-assisted resource optimisation under variable workloads.

## References

Abadi, M. *et al.* (2016) ‘TensorFlow: A system for large-scale machine learning’, *12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16)*, pp. 265–283.

Bernstein, D. (2014) ‘Containers and Cloud: From LXC to Docker to Kubernetes’, *IEEE Cloud Computing*, 1(3), pp. 81–84. doi: 10.1109/MCC.2014.51.

Krizhevsky, A. (2009) *Learning Multiple Layers of Features from Tiny Images*. Technical report. Toronto: University of Toronto.

Lorido-Botran, T., Miguel-Alonso, J. and Lozano, J.A. (2014) ‘A review of auto-scaling techniques for elastic applications in cloud environments’, *Journal of Grid Computing*, 12(4), pp. 559–592. doi: 10.1007/s10723-014-9314-7.

Mao, H., Alizadeh, M., Menache, I. and Kandula, S. (2016) ‘Resource management with deep reinforcement learning’, *Proceedings of the 15th ACM Workshop on Hot Topics in Networks*, pp. 50–56. doi: 10.1145/3005745.3005750.

Rawat, W. and Wang, Z. (2017) ‘Deep convolutional neural networks for image classification: A comprehensive review’, *Neural Computation*, 29(9), pp. 2352–2449. doi: 10.1162/NECO_a_00990.

Sze, V., Chen, Y.-H., Yang, T.-J. and Emer, J.S. (2017) ‘Efficient processing of deep neural networks: A tutorial and survey’, *Proceedings of the IEEE*, 105(12), pp. 2295–2329. doi: 10.1109/JPROC.2017.2761740.
