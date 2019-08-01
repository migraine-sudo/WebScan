# coding:utf-8
"""
 * Name:WebScan
 * User: dreamn
 * Date: 2019-07-06
 * Time: 20:04
 * Description:核心框架，核心逻辑：列出可用模块与全功能网站分析扫描（分成先模块后扫描的机制，或者直接全局体检）
 重点突出：效率，模块化，与算法优化
"""
from WebScan import log, output, model, check, scan,login


def PrintLogo():  # 输出logo
    output.printf("""
         __        __   _    ____                  
         \ \      / ___| |__/ ___|  ___ __ _ _ __  
          \ \ /\ / / _ | '_ \___ \ / __/ _` | '_ \ 
           \ V  V |  __| |_) ___) | (_| (_| | | | |
            \_/\_/ \___|_.__|____/ \___\__,_|_| |_| 
        """, "red")

    output.printf("""
        [*]Written by Dreamn Team
        [*]Ver 1.0.0.1
            """, "blue")


# 输入要测试的url
def input_url():
    url = raw_input("[*]Please enter the website to be tested：")
    if (not check.CheckUrl(url)):
        output.printf("[-]This url looks invalid.Please enter again!", 'bred', 'white')
        return input_url()
    return url


# 输入执行线程数，该数据会延续到下级plugins中
def input_thread_num():
    thread_num = raw_input("[*]Please enter the number of threads(2-50)：")
    if (not check.CheckThread(thread_num)):
        output.printf("[-]This num looks invalid.Please enter again!", 'bred', 'white')
        return input_thread_num()
    return int(thread_num)


# 输入搜索深度
def input_depth():
    depth = raw_input("[*]Please enter scan depth（1-10 The larger the value, the longer the time.）：")
    if (not check.CheckDepth(depth)):
        output.printf("[-]This depth looks invalid.Please enter again!", 'bred', 'white')
        return input_depth()
    return int(depth)


# 输入是否记录日志
def input_islog():
    islog = raw_input("[*]If you want to save log? (Y/N)")
    if islog == "Y":
        islog = True
    else:
        islog = False
    return islog


# 开始扫描
def startscan(url, thread_num, islog, depth,cookie):
    s = scan.scan(url, thread_num, islog, depth,3,cookie)
    # 调用scan模块对网站进行爬取
    result = s.scan()
    # 取得爬取结果result
    return result


# 模块处理
def use_model(model_info, result, thread_num, islog,session):
    output.printf("[*]We provide some modules for further testing. Please select the module.", 'green')
    i = 0
    for v in model_info:
        output.printf("    [" + str(i) + "]" + v["name"] + "   " + v["introduction"])
        i += 1
    n = raw_input("[*]Please enter the numeric serial number：")

    if int(n) not in range(0, i):
        output.printf("[-]Without this option, please try again.", 'red')
        use_model(model_info, result, thread_num, islog,session)
    else:
        output.printf("[*]Using " + model_info[int(n)]["name"] + " module.", 'blue')
        model.run_model(model_info[int(n)]["model"], result, thread_num, islog,session)


if __name__ == "__main__":
    PrintLogo()  # 输出logo
    model = model.models()  # 加载模块信息
    model_info = model.get_models()  # 模块信息

    # 进行输入
    url = input_url()
    depth = input_depth()
    num = input_thread_num()
    islog = input_islog()
    # 输入完成，进行扫描
    session=login.login(url)

    #测试网站模拟登录
    if islog:
        log.write("WebScan", "Start scanning website : " + url)
    result = startscan(url, num, islog, depth,session)
    #再次登陆，保证session有效
    session = login.login(url)


    if result:
        if islog:
            log.write("WebScan", "Scan completed！")
        output.printf("[*]When the scan is completed, the following URLs are found:", 'green')
        for v in result:
            output.printf("    [URL]=>" + v, 'blue')
        use_model(model_info, result, num, islog,session)

    else:
        if islog:
            log.write("WebScan", "Found Nothing！")
        output.printf("[-]Scanning completed, no valid URL was found！", "yellow")
