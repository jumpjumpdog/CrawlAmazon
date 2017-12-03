import redis, re

def saveToRedis():
    r =  redis.Redis(host='192.168.1.100',port=6379,db=0)
    with open("D:\\tools\\movies_form.txt","rb") as f:
        for index, item in enumerate(f):
            # print item
            # if(index==20):
            #     break
            # else:
            if index % 2 == 0:
                item = deleteSpace(item)
                r.set(item,"product")

def deleteSpace(str):
    str = str.replace(" ","")
    str = str.replace("\r\n", "")
    return str

def getKey():
    r = redis.Redis(host="192.168.1.100",port=6379,db=0)
    keys = r.keys()
def trans(file1, file2):
    productId = re.compile(r'(product/productId *):(.*)')
    userId = re.compile(r'(review/userId *):(.*)')
    with open(file1, "rb") as fr:
        with open(file2, "wb") as fw:
            for index, line in enumerate(fr):
                objSearch = productId.search(line)
                # if index == 100:
                #     return
                if objSearch:
                    fw.write(objSearch.group(2)+'\r\n')
                else:
                    objSearch = userId.search(line)
                    if objSearch:
                        fw.write(objSearch.group(2)+'\r\n')

class Redis_Handler():
    def __init__(self):
        self.con = redis.Redis(host="192.168.1.100",port=6379,db=1)

    def execute(self):
        batch_size = 10000
        with open("D:\\tools\\movies_form.txt", "rb") as f:
            try:
                count = 0
                setName = 0
                pipeline_redis = self.con.pipeline()
                for index, line in enumerate(f):
                    if index % 2 == 0:
                        line = deleteSpace(line)
                        count += 1
                        pipeline_redis.sadd(setName,line)
                        if count % 100000 == 0:
                            setName = count/100000
                            print "execute"
                            pipeline_redis.execute()
            except Exception as e:
                print e.message


if __name__ == "__main__":
    redisHandler =  Redis_Handler()
    redisHandler.execute()
    # saveToRedis()