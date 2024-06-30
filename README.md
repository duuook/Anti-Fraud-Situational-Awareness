# 使用指南

使用该系统有两种方式:直接访问远程服务器或是将项目文件clone到本地,在本地端口访问



## 1. 远程访问服务器

可联网环境下,在浏览器(chrome或是edge)中输入以下IP地址+端口号访问,可联系仓库持有者开启云服务器上对应服务使用系统

> [101.36.125.205](http://101.36.125.205:8001/afsa/)



## 2. 本地配置访问

- 将项目文件clone到本地,注意本地是否可以ping通GitHub网站;

	```git
	git clone https://github.com/duuook/Anti-Fraud-Situational-Awareness.git
	```



- clone完成后,开始配置环境,开发过程中使用的python环境为3.11,建议>=3.11.9,最好为虚拟环境运行,具体可以参考Anaconda官网教程

	> [Download Anaconda Distribution | Anaconda](https://www.anaconda.com/download/)



- python成功安装开始安装依赖

    ```python
    // 此时需要使用cmd,并cd至项目一级目录下
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    ```

    由于配置过程中的各异性,依赖大概率安装不全,在运行过程中极大概率出现module not found 的情况,届时请自行安装对应依赖.

    注:数据库在./afsa/settings.py中配置是缺失的,如有需要请联系仓库持有人



- 完成上述准备后,如果使用虚拟环境注意环境切换,输入以下命令即可运行系统

    ```cmd
    // 该命令默认监听本机127.0.0.0:8000,如果需要制定特定端口可在命令末指定,如0.0.0.0:8001
    python manage.py runserver
    ```



