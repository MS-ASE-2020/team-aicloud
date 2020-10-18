## Environment/Architecture

### Production Environment

- Software

  Rishi 预计通过 Container 进行 Web 应用的部署，目标的 Host OS 偏向于 Linux。同时每一个计算任务将运行在一个 Container 中，我们将可能借助 Kubernetes 进行 Container 的管理。

- Hardware

  Rishi 涉及对时间序列预测模型的训练，需要满足在计算量较大情况下的并发需求。初步设计中，当用户量较小时，我们的硬件应至少满足以下条件：

  - 16GB RAM
  - 8 Cores CPU
  - 1TB Storage: 由于需要存储用户任务训练后的模型和数据，因此会需要比较大的存储空间
  - Gigabyte Network: 满足大量数据的上传和下载。

  我们可能会借助云服务商来提供部署平台。

### Architecture Design

#### 分层设计

Rishi 将大致分为三层，其中一层为前端，将负责与用户进行交互，并向后端请求和返回数据。后端则将分为两部分，其中一部分是网络应用中 Django 为核心的一层，主要负责用户请求的处理和页面数据的返回。另外一部分是项目的核心部分，将负责计算任务的分发和执行，需要进行最佳参数的搜索和模型的训练。这一部分计算任务将运行在独立的 Container 中，并通过 Contrainer Manager (如 Kubernetes) 进行管理。

![](./assets/rishi_arch.svg)

#### 模块子系统设计

Rishi 将主要分成以下模块：

- User interface
- Input module
- Data pre-processing module
- Model execution and parameter search module
- Output module

## Interface/Interaction

### 程序接口



## Process/Threading

Rishi 由于是个 Web App，其在 Web Server 部分的并发将主要由 Django Framework 来负责。

而此项目的核心是提供时间序列预测任务的 Training 和 Inference，涉及到大量的计算任务，因此需要比较完整的并发支持，包括资源限制，负载平衡。我们预计将通过容器的方式提供此部分任务的运行环境。并通过 Kubernetes 进行管理。

