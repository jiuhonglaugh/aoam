

    ###配置文件说明
    config/hadoop(配置文件直接从hadoop安装目录下拉取)
        其中包括    core-site.xml、hdfs-site.xml、mapred-site.xml、yarn-site.xml、slaves
    config/hbase(配置文件直接从hadoop安装目录下拉取)
        其中包括    habse-site.xml、regionservers
    config/application.properties
        [zookeeper]
            zookeeper.hosts=IP:PORT,IP:PORT
        [kafka]
            kafka.hosts=IP:PORT,IP:PORT
            kafka.start.script=             'Kafka家目录下对应启动脚本'
            kafka.process.number=           '单个节点上有多少个Kafka进程实例'
        [azkaban]
            azkaban.web.hosts=IP:PORT,IP:PORT
            azkaban.exe.hosts=IP:PORT,IP:PORT
        [hive]
            hive.server2=IP:PORT,IP:PORT
            hive.metastore=IP:PORT,IP:PORT
            hive.metastore.start.script=    'Hive家目录下对应的启动脚本'
            hive.server2.start.script=      'Hive家目录下对应的启动脚本'
        [elasticsearch]
            es.hosts=IP:PORT,IP:PORT,IP:PORT
        [storm]
            storm.hosts.nimbus=IP:PORT,IP:PORT
            storm.hosts.supervisor=IP:PORT,IP:PORT
        [logstash]
            logstash.hosts=IP:PORT,IP:PORT
        [flume]
            flume.hosts=IP,IP
        [tomcat]
            tomcat.hosts=IP:PORT,IP:PORT
            tomcat.process.number=1,1        '单个节点上有多少个Tomcat进程实例'
            tomcat.start.script.path=        'Tomcat 启动脚本路径'
###调用逻辑
    sbin/start-All.sh
        sbin/start-backend.sh
            bin/tomcat.py
                utils/目录下工具类
                    读取
                        config/目录下配置文件

        sbin/start-bigdata.sh
            bin/azkaban.py
            bin/elasticsearch.py
            bin/flume.py
            bin/hadoop.py
            bin/hbase.py
            bin/hive.py
            bin/kafka.py
            bin/logstash.py
            bin/storm.py
            bin/tomcat.py
            bin/zookeeper.py
                utils/目录下工具类
                    读取
                        config/目录下配置文件
