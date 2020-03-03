

配置文件说明
    config/hadoop(配置文件直接从hadoop安装目录下拉取)
        其中包括    core-site.xml、hdfs-site.xml、mapred-site.xml、yarn-site.xml、slaves
    config/hbase(配置文件直接从hadoop安装目录下拉取)
        其中包括    habse-site.xml、regionservers
    config/application.properties



调用逻辑
    sbin/start-All.sh
        调用
            sbin/start-backend.sh
                调用
                    bin/tomcat.py
                        调用
                            utils/目录下工具类
                                读取
                                    config/目录下配置文件

            sbin/start-bigdata.sh
                调用
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
                        调用
                            utils/目录下工具类
                                读取
                                    config/目录下配置文件