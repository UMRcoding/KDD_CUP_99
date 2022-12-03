# 开源项目说明

**目的：学术研究**

如果您遇到任何安装或使用问题，可以通过QQ或issue的方式告诉我。同时使用本项目写论文或做其它学术研究的朋友，如果想把自己的研究成果展示在下面，也可以通过QQ或issue的方式告诉我。看到的小伙伴记得点点右上角的Star~

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032308792.png)



# KDD_CUP 99日志集分析

本实验描述的项目是KDD_CUP 99日志集，KDD CUP是ACM年度竞赛。KDD 99 就是这个竞赛在1999年使用的数据集。这个数据集是林肯实验室建立了模拟美国空军局域网的网络环境，收集了 9 周的网络连接和系统审计数据，仿真各种用户类型、各种不同的网络流量和攻击手段。

本实验首先对系统进行需求分析，进行数据分析，数据集的分析和提取特征，包括攻击类型分布，协议分类分布，连接持续时间的分布，并绘制pyplot图表。并进行有监督的机器学习，对数据进行分类预测。



## 一、实训目的

### 网络行为分析实训目的

- 网络日志数据结构解析，明确流量分析目标

- 数据探索性分析
- 提取网络流量分析的指标体系
- 实现基于Python的网络流量日志分析及可视化实现



### 选题分析

#### 数据来源

[KDD Cup 99数据集](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)



#### 数据特征描述

一个网络连接定义为在某个时间内从开始到结束的TCP数据包序列，并且在这段时间内，数据在预定义的协议下（如TCP、UDP）从源IP地址到目的IP地址的传递。每个网络连接被标记为正常（normal）或异常（attack），异常类型被细分为4大类共39种攻击类型，其中22种攻击类型出现在训练集中，另有17种未知攻击类型出现在测试集中。

- KDD99数据集总共由500万条记录构成，它提供10%的训练子集和测试子集，训练子集和测试子集分别为KDD99数据集中的10%训练样本和corrected 的测试样本
- “ / ” 表示该种攻击类型只在测试集（或训练集）中出现，而未在训练集（或测试集）中出现；
- 训练集中共出现了22个攻击类型，而剩下的17种只在测试集中出现，这样设计的目的是检验分类器模型的泛化能力，对未知攻击类型的检测能力是评价入侵检测系统好坏的重要指标。



四种异常类型分别是：

| 标识类型 | 含义                                 | 具体分类标识                                                 |
| :------- | :----------------------------------- | ------------------------------------------------------------ |
| Dos      | 拒绝服务攻击                         | back、land、neptune、pod、smurf、teardrop                    |
| Probing  | 监视和其他探测活动                   | ipsweep、nmap、portsweep、satan                              |
| R2L      | 来自远程机器的非法访问               | ftp_write、guess_passwd、imap、multihop、phf、spy、warezclient、warezmaster |
| U2R      | 普通用户对本地超级用户特权的非法访问 | buffer_overflow、loadmodule、perl、rootkit                   |



####  数据标识

- [kddcup.names](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names)	功能列表。
- [kddcup.data.corrected](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data.gz)     完整数据集（18M；743M 未压缩）
- [kddcup.data_10_percent.gz](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz)      10% 的子集。（2.1M；75M 未压缩）
- [kddcup.newtestdata_10_percent_unlabeled.gz](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.newtestdata_10_percent_unlabeled.gz)     （1.4M；45M 未压缩）
- [kddcup.testdata.unlabeled.gz](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.testdata.unlabeled.gz)     （11.2M；430M 未压缩）
- [kddcup.testdata.unlabeled_10_percent.gz](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.testdata.unlabeled_10_percent.gz)     （1.4M；45M 未压缩）
- [corrected.gz](http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz)     使用更正标签测试数据。
- [training_attack_types](http://kdd.ics.uci.edu/databases/kddcup99/training_attack_types)     入侵类型列表。
- [typo-correction.txt](http://kdd.ics.uci.edu/databases/kddcup99/typo-correction.txt)     关于数据集中已纠正的错字的简要说明 (6/26/07)



#### 数据内容

KDD99数据集中每个连接用41个特征来描述，加上最后的标记（label），一共有42项，其中前41项特征分为4大类，下面按顺序解释各个特征的含义：

**一、TCP连接的基本特征(1-9)**
基本连接特征包含了一些连接的基本属性，如连续时间，协议类型，传送的字节数等。

1. duration. 连接持续时间，以秒为单位，连续类型。范围是 [0, 58329] 。它的定义是从TCP连接以3次握手建立算起，到FIN/ACK连接结束为止的时间；若为UDP协议类型，则将每个UDP数据包作为一条连接。数据集中出现大量的duration = 0 的情况，是因为该条连接的持续时间不足1秒。

2. protocol_type. 协议类型，离散类型，共有3种：TCP, UDP, ICMP。

3. service. 目标主机的网络服务类型，离散类型，共有70种。’aol’, ‘auth’, ‘bgp’, ‘courier’, ‘csnet_ns’, ‘ctf’, ‘daytime’, ‘discard’, ‘domain’, ‘domain_u’, ‘echo’, ‘eco_i’, ‘ecr_i’, ‘efs’, ‘exec’, ‘finger’, ‘ftp’, ‘ftp_data’, ‘gopher’, ‘harvest’, ‘hostnames’, ‘http’, ‘http_2784′, ‘http_443′, ‘http_8001′, ‘imap4′, ‘IRC’, ‘iso_tsap’, ‘klogin’, ‘kshell’, ‘ldap’, ‘link’, ‘login’, ‘mtp’, ‘name’, ‘netbios_dgm’, ‘netbios_ns’, ‘netbios_ssn’, ‘netstat’, ‘nnsp’, ‘nntp’, ‘ntp_u’, ‘other’, ‘pm_dump’, ‘pop_2′, ‘pop_3′, ‘printer’, ‘private’, ‘red_i’, ‘remote_job’, ‘rje’, ‘shell’, ‘smtp’, ‘sql_net’, ‘ssh’, ‘sunrpc’, ‘supdup’, ‘systat’, ‘telnet’, ‘tftp_u’, ‘tim_i’, ‘time’, ‘urh_i’, ‘urp_i’, ‘uucp’, ‘uucp_path’, ‘vmnet’, ‘whois’, ‘X11′, ‘Z39_50′。

4. flag. 连接正常或错误的状态，离散类型，共11种。’OTH’, ‘REJ’, ‘RSTO’, ‘RSTOS0′, ‘RSTR’, ‘S0′, ‘S1′, ‘S2′, ‘S3′, ‘SF’, ‘SH’。它表示该连接是否按照协议要求开始或完成。例如SF表示连接正常建立并终止；S0表示只接到了SYN请求数据包，而没有后面的SYN/ACK。其中SF表示正常，其他10种都是error。

5. src_bytes. 从源主机到目标主机的数据的字节数，连续类型，范围是 [0, 1379963888]。

6. dst_bytes. 从目标主机到源主机的数据的字节数，连续类型，范围是 [0. 1309937401]。

7. land. 若连接来自/送达同一个主机/端口则为1，否则为0，离散类型，0或1。

8. wrong_fragment. 错误分段的数量，连续类型，范围是 [0, 3]。

9. urgent. 加急包的个数，连续类型，范围是[0, 14]。



**二、TCP连接的内容特征（共13种）10-22**
对于U2R和R2L之类的攻击，由于它们不像DoS攻击那样在数据记录中具有频繁序列模式，而一般都是嵌入在数据包的数据负载里面，单一的数据包和正常连接没有什么区别。为了检测这类攻击，Wenke Lee等从数据内容里面抽取了部分可能反映入侵行为的内容特征，如登录失败的次数等。

10. hot. 访问系统敏感文件和目录的次数，连续，范围是 [0, 101]。例如访问系统目录，建立或执行程序等。
11. num_failed_logins. 登录尝试失败的次数。连续，[0, 5]。
12. logged_in. 成功登录则为1，否则为0，离散，0或1。
13. num_compromised. compromised条件（**）出现的次数，连续，[0, 7479]。
14. root_shell. 若获得root shell 则为1，否则为0，离散，0或1。root_shell是指获得超级用户权限。
15. su_attempted. 若出现”su root” 命令则为1，否则为0，离散，0或1。
16. num_root. root用户访问次数，连续，[0, 7468]。
17. num_file_creations. 文件创建操作的次数，连续，[0, 100]。
18. num_shells. 使用shell命令的次数，连续，[0, 5]。
19. num_access_files. 访问控制文件的次数，连续，[0, 9]。例如对 /etc/passwd 或 .rhosts 文件的访问。
20. num_outbound_cmds. 一个FTP会话中出站连接的次数，连续，0。数据集中这一特征出现次数为0。
21. is_hot_login.登录是否属于“hot”列表（***），是为1，否则为0，离散，0或1。例如超级用户或管理员登录。
22. is_guest_login. 若是 guest 登录则为1，否则为0，离散，0或1。



**三、基于时间的网络流量统计特征 （共9种，23～31）**
由于网络攻击事件在时间上有很强的关联性，因此统计出当前连接记录与之前一段时间内的连接记录之间存在的某些联系，可以更好的反映连接之间的关系。这类特征又分为两种集合：一个是 “same host”特征，只观察在过去两秒内与当前连接有相同目标主机的连接，例如相同的连接数，在这些相同连接与当前连接有相同的服务的连接等等；另一个是 “same service”特征，只观察过去两秒内与当前连接有相同服务的连接，例如这样的连接有多少个，其中有多少出现SYN错误或者REJ错误。

23. count. 过去两秒内，与当前连接具有相同的目标主机的连接数，连续，[0, 511]。
24. srv_count. 过去两秒内，与当前连接具有相同服务的连接数，连续，[0, 511]。
25. serror_rate. 过去两秒内，在与当前连接具有相同目标主机的连接中，出现“SYN” 错误的连接的百分比，连续，[0.00, 1.00]。
26. srv_serror_rate. 过去两秒内，在与当前连接具有相同服务的连接中，出现“SYN” 错误的连接的百分比，连续，[0.00, 1.00]。
27. rerror_rate. 过去两秒内，在与当前连接具有相同目标主机的连接中，出现“REJ” 错误的连接的百分比，连续，[0.00, 1.00]。
28. srv_rerror_rate. 过去两秒内，在与当前连接具有相同服务的连接中，出现“REJ” 错误的连接的百分比，连续，[0.00, 1.00]。
29. same_srv_rate. 过去两秒内，在与当前连接具有相同目标主机的连接中，与当前连接具有相同服务的连接的百分比，连续，[0.00, 1.00]。
30. diff_srv_rate. 过去两秒内，在与当前连接具有相同目标主机的连接中，与当前连接具有不同服务的连接的百分比，连续，[0.00, 1.00]。
31. srv_diff_host_rate. 过去两秒内，在与当前连接具有相同服务的连接中，与当前连接具有不同目标主机的连接的百分比，连续，[0.00, 1.00]。

注：这一大类特征中，23、25、27、29、30这5个特征是 “same host” 特征，前提都是与当前连接具有相同目标主机的连接；24、26、28、31这4个特征是 “same service” 特征，前提都是与当前连接具有相同服务的连接。



**四、基于主机的网络流量统计特征 （共10种，32～41）**
基于时间的流量统计只是在过去两秒的范围内统计与当前连接之间的关系，而在实际入侵中，有些 Probing攻击使用慢速攻击模式来扫描主机或端口，当它们扫描的频率大于2秒的时候，基于时间的统计方法就无法从数据中找到关联。所以Wenke Lee等按照目标主机进行分类，使用一个具有100个连接的时间窗，统计当前连接之前100个连接记录中与当前连接具有相同目标主机的统计信息。

32. dst_host_count. 前100个连接中，与当前连接具有相同目标主机的连接数，连续，[0, 255]。
33. dst_host_srv_count. 前100个连接中，与当前连接具有相同目标主机相同服务的连接数，连续，[0, 255]。
34. dst_host_same_srv_rate. 前100个连接中，与当前连接具有相同目标主机相同服务的连接所占的百分比，连续，[0.00, 1.00]。
35. dst_host_diff_srv_rate. 前100个连接中，与当前连接具有相同目标主机不同服务的连接所占的百分比，连续，[0.00, 1.00]。
36. dst_host_same_src_port_rate. 前100个连接中，与当前连接具有相同目标主机相同源端口的连接所占的百分比，连续，[0.00, 1.00]。
37. dst_host_srv_diff_host_rate. 前100个连接中，与当前连接具有相同目标主机相同服务的连接中，与当前连接具有不同源主机的连接所占的百分比，连续，[0.00, 1.00]。
38. dst_host_serror_rate. 前100个连接中，与当前连接具有相同目标主机的连接中，出现SYN错误的连接所占的百分比，连续，[0.00, 1.00]。
39. dst_host_srv_serror_rate. 前100个连接中，与当前连接具有相同目标主机相同服务的连接中，出现SYN错误的连接所占的百分比，连续，[0.00, 1.00]。
40. dst_host_rerror_rate. 前100个连接中，与当前连接具有相同目标主机的连接中，出现REJ错误的连接所占的百分比，连续，[0.00, 1.00]。
41. dst_host_srv_rerror_rate. 前100个连接中，与当前连接具有相同目标主机相同服务的连接中，出现REJ错误的连接所占的百分比，连续，[0.00, 1.00]。



## 二、需求分析

### 数据源特征分析

- 查看所有连接持续时间平均值，四分位数信息
- 查看协议类型排行榜，TCP, UDP, ICMP各自比例
- 对数据集中异常类型数量进行统计
- 查看异常类型各自的占比

```
1. df.describe() # 查看所有数据平均值，四分位数等信息
2. df.info() # 查看所有数据的数据类型和非空值个数。
3. df.shape # 查看数据行列数
4. df.isnull().sum() # 查看数据各个特征为空值的个数
1. 集中趋势：均值，中位数，众数。对于正态分布的数据，均值的效果比较好，而对于有偏数据，因为存在极值，所有会对均值产生影响，此时，用中位数去进行集中趋势的描述。
2. 离散程度：方差和标准差。这两个用哪个都可，不过标准差是具有实际意义的。另外，还可以用极差，平均差，四分位差，离散系数（针对多组数据离散程度的对比）。
```



**对连续数据可视化有：**

1. **直方图。可以大致看出数据的分布情况，但会受限于bins的取值并且图形不光滑。可在直方图上再画出核密度图(KDE)，进行更详细的查看。**
2. **核密度图**
3. **箱线图。反映原始数据的分布特征，还能进行多组数据的比较。可看出数据的离群点。**
4. **散点图。利用索引和连续数据作散点图，直观看数据是否随机。**

**对离散数据可视化主要有：**

1. **饼图。对于查看数据结构比较直观，所占百分比。**
2. **柱形图。对各类别出现次数进行可视化。可排序，这样观察数据更直观。**



### 网络行为特征分析

- 用户登录情况
- root用户访问比例
- 异常类型各自的比例



## 三、网络行为特征分析

### 特征分析

#### 连接状态统计

对数据集中正常连接和非正常连接数量进行统计，正常连接和非正常连接都是风控模型的研究对象。经过统计，该数据集中正常连接 97278 次，非正常连接 396743 次，非正常连接比正常连接多 299,465 次。可见该数据集中存在大量的异常连接。连接状态统计如图一所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152104.png)



#### 异常连接的分布

Smurf攻击 通过将回复地址设置成受害网络的广播地址的ICMP应答请求(ping)数据包，来淹没受害主机，最终导致该网络的所有主机都对此ICMP应答请求做出答复，导致网络阻塞。这种攻击只有在服务器在收到 SYN 后分配资源，但在收到 ACK 之前这个区段有效。

neptune攻击 是一种拒绝服务攻击，发生该攻击时目标主机会收到大量的SYN报文，进而影响目标主机的正常运行。

对非正常连接进行数据统计，对各种异常进行初次分类，再次分类统计后，得到 TOP异常统计图 。其中 smurf 攻击有 280790 次， neptune 攻击有 107201 次，这两种攻击总和占所有非正常连接的 97.79%，其他类型攻击仅有 8752次， 约占非正常连接样本比例 2.205%。异常连接的分布如图二所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152105.png)

由 TOP 异常连接图可知，neptune攻击 和 Smurf攻击 占所有非正常连接的 97.79%，所以需要先全力解决这两个攻击。当主机受到neptune攻击时，该主机收到大量的SYN请求，因此由此发生的会话数远高于正常情况下的会话数目。neptune攻击利用TCP协议的缺陷，通过发送大量的半连接请求，耗费CPU和内存资源。

**neptune攻击防范**

1. SYN 缓存技术：修改TCP服务器端的三次握手协议，在TCP服务器收到TCP syn包并返回TCP SYN+ACK包时，不分配一个专门的数据区，而是根据这个SYN包计算出一个cookie值，在收到TCP ACK包时，TCP 服务器在根据那个cookie值检查这个TCP ACK包的合法性。如果合法，再分配专门的数据区进行处理未来的TCP连接。最常用的一个手段就是优化主机系统设置。比如降低SYN timeout时间，使得主机尽快释放半连接的占用或者采用SYN cookie设置，如果短时间内收到了某个IP的重复SYN请求，我们就认为受到了攻击。
2. SYN  Cookie技术，将 SYN cookies 定义为“TCP 服务器进行的对开始TCP数据包序列数字的特定选择”。SYN Cookies 的应用允许服务器当 SYN 队列被填满时避免丢弃连接。相反，服务器会表现得像 SYN 队列扩大了一样。服务器会返回适当的 SYN+ACK 响应，但会丢弃 SYN 队列条目。如果服务器接收到客户端随后的ACK响应，服务器能够使用编码在 TCP 序号内的信息重构 SYN 队列条目。
3. 合理的采用防火墙设置等外部网络进行拦截，或限定某一段时间内来自同一来源请求新连线的数量。

**Smurf攻击防范**

1. 配置主机和路由器忽略源地址为广播地址的数据包。或将路由器配置为不转发定向到广播地址的数据包。
2. ISP 实施入口过滤，根据伪造的源地址拒绝攻击数据包。



#### 异常类型

除 smurf 和 neptune 攻击外，其他攻击所占比例如下表所示。其中 back 攻击 占比相对较多。异常类型的分布如图三所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152102.png)



#### 不同协议与发送/接收的关系

通过 Pandas 的 pivot_table 函数，即数据透视表，可以观察不同函数的连接持续时间，发送字节数，接受字节数关系。其中 ICMP 平均连接持续时间为 0 秒，这是因为该条连接的持续时间不足1秒，而数据集只精确到了秒级的时间精度。从源主机到目标主机的数据的 平均 字节数约为 928 字节，从目标主机到源主机的数据的字节数 的 平均 字节数约为 0 字节 。不同协议与发送/接收平均占比如图四所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152110.png)

通过数据透视表调查最小值，其中 ICMP 平均连接持续时间为 0 秒，从源主机到目标主机的数据的 最小 字节数为 8 字节，从目标主机到源主机的数据的字节数 的 最小 字节数约为 0 字节。结果如下图。不同协议与发送/接收最小值如图五所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152111.png)

再次通过数据透视表调查最大值，其中 ICMP 平均连接持续时间为 0 秒，从源主机到目标主机的数据的 最大字节数为 1480字节，从目标主机到源主机的数据的字节数 的 最大 字节数为 0 字节。结果如下图。不同协议与发送/接收最大值如图六所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152112.png)



#### 用户登录失败情况

用户登录，即电脑用户进行身份验证或为进入某一项程序而进行的一项基本操作，以便该用户可以在该网站上进行相应的操作。经统计，异常状况时用户登录情况，成功占据大多数，其中包含：1. 在正常的网络环境中，用户的登录请求发生非致命异常。2. 在异常的网络环境中，用户本人直接进行登录。3. 非信任方已知用户正确密码，直接进行登陆验证的情况。用户登录结果情况如图七所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152836.png)



#### root用户访问占比

Root，也称为根用户，是系统中的唯一的超级用户，具有系统中的最高权限。在异常网络环境中，root用户访问次数为 57 次，数值等于用户登录失败次数。所以可以说，在异常网络环境中用户登录失败都是处于对于 root 身份的登录请求。root用户访问次数如图八所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152857.png)







### 网络行为分析算法

#### KNN模型

KNN 即 K 最近邻，就是K个最近的邻居，每个样本都可以用它最接近的K个邻近值来代表。近邻算法就是将数据集合中每一个记录进行分类的方法 [1] 。

**KNN的主要优点有：**

1. 理论成熟，思想简单，既可以用来做分类也可以用来做回归。
2. 天然解决多分类问题，也可用于回归问题
3. 和朴素贝叶斯之类的算法比，对数据没有假设，准确度高，对异常点不敏感
4. 由于KNN方法主要靠周围有限的邻近的样本，而不是靠判别类域的方法来确定所属类别的，因此对于类域的交叉或重叠较多的待分样本集来说，KNN方法较其他方法更为适合

**KNN的主要缺点有：**

1. 计算量大，效率低。即使优化算法，效率也不高。
2. 高度数据相关，样本不平衡的时候，对稀有类别的预测准确率低。
3. 相比决策树模型，KNN模型可解释性不强。
4. 维度灾难：随着维度的增加，“看似相近”的两个点之间的距离越来越大，而knn非常依赖距离。

我将设计一个 KNN模型，用来对发送字节数进行预测。先提取样本数据：发送字节数。有许多特征与发送字节数无关，所以需要手动抽取关联特征。我提取出以下特征进行简单实验。

| **持续时间** |   **协议类型**    | **接收字节数** | **加急包个数** |
| :----------: | :---------------: | :------------: | :------------: |
| **duration** | **protocol_type** | **dst_bytes**  |   **urgent**   |

此时共有 444618 rows × 4 columns 数据，需要对进行数据集拆分。关于 test_size 的选择，理论上来说，我们是要用数据集中的数据来建模的，因此训练集占比越大，所建模型会越接近，但是此时会显得测试集数据过少，测试结果不具有普遍性。因此需要根据实际情况来选择，一般情况下会选择 15% 左右的数据作为测试集。我将以 15% 比例的数据作为测试集数据。

拆分后观察样本数据中的特征是否需要特征工程。其中协议类型为非数值型数据，需要特征值化，转换为数值型数据。样本数据如图九所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152880.png)

对训练集特征进行手动onehot编码，并将 occ_one_hot 与 x_train 进行级联。同样对测试集特征进行手动 onehot 编码，并对测试集进行级联。onehot 编码后数据结果如图十所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152904.png)



#### 探索模型训练最适线程数

线程多了可以提高程序并行执行的速度，但是并不是越多越好。给定过多进程对速度提升基本没有贡献。其一，每个线程都要占用内存，多线程就意味着更多的内存资源被占用。其二，从微观上讲，cpu 必须不断的在各个线程间快回更换执行，线程间的切换无意间消耗了许多时间，所以 cpu 有效利用率反而是下降的。

一般多线程的效率很难达到 100%。如下图，在指定线程数小于 8 时，给定的线程越多，利用起来的线程也越多，但整体利用率是越来越低的。测试电脑是最多 8 线程。在 8 线程时，固定 KNN 邻近参数为10，此时系统利用率占用如图十一所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152925.png)



探索最适线程数核心代码如下：

```python
# 用学习曲线，寻找最适线程数
for i in range(1,9):
    start_time = time.perf_counter()
    # 实例化
    knn = KNeighborsClassifier(n_neighbors=10, n_jobs = i)
    # 训练模型
    knn.fit(x_train, y_train)
    # 训练好模型后进行评分
    score = knn.score(x_test, y_test)
    end_time = time.perf_counter()
    # 拿到不同threads的时间
    scores.append(score)
    threads.append(i)
    times.append(end_time-start_time)
```



模型训练一次的花费时间与线程数关系如下图。可见在给定的线程数时，随着线程数增加，时间逐渐减少，尤其是在线程数从 1-4 的过程中，下降幅度更明显。
（因为测试电脑只有8个核心，不知道这里的节点 8 以后的是否是受此影响，还需要后续在服务器更多测试来判断。如果是这样，对我的指导是设定的线程数不应该超过CPU的核心数。模型训练时间与线程数关系如图十二所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152948.png)

模型得分与线程数关系如下图。可见不同线程是不影响程序输出的，不同线程数目不影响对于模型训练的评分。模型训练得分与线程数关系如图十三所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152383.png)



#### **优化KNN模型，探索最适模型超参数**

进行无量纲化，将不同规格的数据转换到同一规格，无量纲化可以加快求解速度。K近邻中无量纲化可以帮我们提升模型精度，避免某一个取值范围特别大的特征对距离计算造成影响。在特征抽取后我们就可以获取对应的数值型的样本数据啦，然后就可以进行数据处理。通过特定的统计方法（数学方法)，将数据转换成算法要求的数据。

标准化指当数据按均值中心化后，再按标准差缩放，数据就会服从为均值为0，方差为1的正态分布(即标准正态分布)，而这个过程，就叫做数据标准化。至于 StandardiScaler 和 MinMaxScaler 的选择，在大多数机器学习算法中，普遍会选择 StandardScaler 来进行特征缩放，因为 MinMaxScaler 对异常值非常敏感。这里我选择 StandardScaler 进行标准化。

```python
# 标准化
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
data = [anomalies_count]
ss.fit_transform(data)
```

KNN 分类模型通过测量不同特征值之间的欧氏距离（多维空间的绝对距离）进行分类。K 的不同会直接导致分类结果的不同。k值选取要适宜，k过大会导致模型简化而失去意义，k值过小则会将模型复杂化并产生过拟合现象。且k最好为奇数，以免出现结果相等的尴尬情况。K值一般取一个比较小的数值，例如采用交叉验证法（简单来说，就是一部分样本做训练集，一部分做测试集）来选择最优的K值。

探索最适K值核心代码如下：

```python
# 用学习曲线，寻找最优K值
for i in range(1,51):
    # 实例化
    knn = KNeighborsClassifier(n_neighbors=i, n_jobs = -1)
    # 训练模型
    knn.fit(x_train, y_train)
    # 训练好模型后进行评分
    score = knn.score(x_test, y_test)
    # 拿到不同K的得分
    scores.append(score)
    ks.append(i)
end_time=time.perf_counter()
print("Running time:",(end_time-start_time))  #输出程序运行时间
```

经过 85分钟 的 50次 寻找，发现最优的 K 为 29，对应训练得分为 73.13%。未交叉验证下，模型训练得分与超参数关系如图十四所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152415.png)



#### **使用KNN模型，对发送字节数进行预测**

用训练好的模型对发送字节数进行预测。未交叉验证下，预测结果如图十五所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152442.png)



#### K折交叉验证

使用交叉验证可以选出最为适合的模型超参数的取值，然后将超参数的值作用到模型的创建中。交叉验证是将样本的训练数据交叉的拆分出不同的训练集和验证集，使用交叉拆分出不同的训练集和验证集测分别试模型的精准度，然后求出的精准度的均值就是此次交叉验证的结果。

经过K折交叉验证后，如图十六所示，模型得分为 92 分

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152568.png)



#### 获取交叉验证超参数

将交叉验证作用到不同的超参数中，选取出精准度最高的超参数作为模型创建的超参数。测试不同超参数的验证结果。

核心代码如下：

```python
scores = []
ks = []
for k in range(2,10):
    knn = KNeighborsClassifier(n_neighbors=k)
    score = cv.cross_val_score(knn, x_train, y_train, cv=6, n_jobs=-1).mean()
    scores.append(score)
    ks.append(k)
```

由于带有交叉验证的训练一次需要一个小时，写好的循环在这里仅仅进行了一轮尝试。在交叉验证下，模型训练得分为 91 分。



#### 使用KNN模型，检测 Neptune

```
knn.predict([[0.0,0.0,1.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0,0.0,0.0]])
```

检测结果如图十八所示。

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152602.png)

检验：

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152628.png)

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212032152900.png)



## 总结

在训练模型中，每次训练都会有警告程序，这在之前的测试中也遇到过。这是因为最初我的超参数设定为 8 折，也就是说 1/8 作为测试集，另外的 7/8 作为训练集。k 折验证是保留比例的，那么在测试集里面 0 平均分成 7 份，显然不能给出小数个 0 样本，所以在 k 折训练中是不成立的。如果一定要 7 折，那就至少要 7 个 0 。带着警告程序也能运行， 只是说无法保证每一折实验中数据都是根据标签的严格比率进行划分实验，实际影响不大。KNN 只是一种缓慢的算法，因为计算图像之间的距离在规模上很困难。所以超参数的选取对于 KNN 至关重要。

在查看攻击网站的日志时，我会想作为运维如何快速确定危害暴露的范围。不同的攻击会有不同的日志记录特点，通过分析日志记录的模型就可以快速找出攻击类型。对于实在无法在第一时间修补该漏洞时，避免进一步损失，也可以选择第三方相关产品和服务的安全保护。



## 参考文献

<span name = "ref1">[1] 维基百科. SYN_flood[EB/OL]. 网址：https://zh.m.wikipedia.org/wiki/SYN_flood</span>

<span name = "ref2">[2] 维基百科.  Smurf_attack [EB/OL]. 网址：https://en.wikipedia.org/wiki/Smurf_attack</span>

<span name = "ref3">[3] 百度百科. 邻近算法[EB/OL]. 网址：https://baike.baidu.com/item/%E9%82%BB%E8%BF%91%E7%AE%97%E6%B3%95/1151153?fromtitle=knn&fromid=3479559&fr=aladdin</span>

<span name = "ref4">[4] apache官方操作手册.  Lookups方法及参数介绍  [EB/OL]. 网址：https://logging.apache.org/log4j/2.x/manual/lookups.html</span>

<span name = "ref5">[5] 卡内基梅隆大学 软件工程学院 数据集 [EB/OL]. 网址：https://resources.sei.cmu.edu/library/asset-view.cfm?assetID=496170</span>

<span name = "ref6">[6] GitHub. 开源工具 TideFinger [EB/OL]. 网址：https://github.com/TideSec/TideFinger</span>





