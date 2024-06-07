# Anti-Fraud-Situational-Awareness（AFSA）前端设计文档



> 运行环境：Ubuntu 20.04、1C1G+40G轻量应用级云主机、腾讯云云数据库

## 一. 网站页面层次设计



### 1.1 功能分析，初步建立分块实现思路

由课程设计要求文档所述，**AFSA系统**需要实现以下功能

> - 信息库建立（database）：
>   - 诈骗电话号码库
>   - 诈骗邮箱库
>   - 诈骗网址库
> - 查询端口建立（search entrance/analysis result）：
>   - 电话号码查询
>   - 邮箱查询
>   - 网站分析
>   - 文本分析



因此前端至少需要两个**页面/URL**路径来实现展示，而从用户易用性角度来看还需要一个**索引页面（index）**来进行用户指引，因此首先需要实现三个页面呈现

> /index
>
> /database/?
>
> /analysis_result/?



### 1.2 页面功能分化

首先是**/database/?**，由于信息库庞杂，如果三个数据库信息都存放在同一页面进行展示则对内存以及读取速率有一定的要求，所以使用响应式页面跳转实现多表之间的数据呈现，首先查看数据库设计

```javascript
SE_db
	- phonenumber 	//电话号码表
	- website 		//网址表
	- msg 			//短信内容表
```



目前的数据表有电话号码、网址、短信内容三个，因此由索引页面出发设计三个表的展示页面

> - /index/
>   - /index/fraud_phonenumber_list/
>   - /index/fraud_ip_list/
>   - /index/frauud_msg_list/
> - /analysis_result



同时分析报告页面由**index**页面中的搜索引出，因此**analysis_result**也应该在index索引之中

> - /index/
>   - /index/fraud_phonenumber_list/
>   - /index/fraud_ip_list/
>   - /index/frauud_msg_list/
>   - /index/analysis_result



### 1.3 用户易用性功能设计

目前简单实现了概要设计说明书中的功能要求，但是从用户易用性角度出发并不是最好的设计。在流程设计上，用户首先接触到的是**index**页面，可以实施两种行为：

- 通过输入框输入想要查询的内容进入**analysis_result**页面，获取查询内容的诈骗系数分析；
- 通过三个按钮进入三个页面浏览信息库内容。



但是对于系统的目标用户来说，尽管多数时候可能是一次性查询行为，但是数据没有长时存在的话对于后续重新查看或者维护都不太方便，因此还需要实现一个历史查询分析报告功能，这一部分内容的实现可以通过数据库存储数据或者是云主机端本地调取html文件传输渲染，这是一个悬而未决的难点

- [ ] 历史查询功能实现

