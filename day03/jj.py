def main():
    info = MyMysql('localhost', 3306, 'root', '123456', 'spider', 'utf8')
    flag = False
    while True:
        try:
            with open('page_number.txt', 'r', encoding='utf8') as f:
                page = int(f.read())
            break
        except Exception as e:
            print(e)
            with open('page_number.txt', 'w', encoding='utf8') as f:
                page_init = '1'
                f.write(page_init)

    while not flag:

        url = "https://list.mogujie.com/search?callback=jQuery21108699047435855352_1540364464262&_version=8193&ratio=3%3A4&cKey=15&page="+str(page)+"&sort=pop&ad=0&fcid=50020&action=trousers&acm=3.mce.1_10_1hepu.109731.0.9XpX0r7nmiyv8.pos_0-m_406085-sd_119-mf_15261_1047900-idx_0-mfs_34-dm1_5000&ptp=1._mf1_1239_15261.0.0.qDoEBgqx&_=1540364464273"
        try:
            html = get_one_page(url)
        except Exception as e:
            with open('page_number.txt', 'w', encoding='utf8') as f:
                f.write(str(page))
            print(e)
            break
        html_content = get_real_content(html)
        # print(html_content)
        result = json.loads(html_content)
        goods_info = result['result']['wall']['docs']
        print(goods_info)
        flag = result['result']['wall']['isEnd']
        for i in goods_info:
            sql = 'insert into ajaxmogu(tradeItemId, img, clientUrl, link, acm, title, cparam, orgPrice, sale, cfav, price, similarityUrl) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (i['tradeItemId'], i['img'], i['clientUrl'], i['link'], i['acm'], i['title'], i.get('cparam') if i.get('cparam') else '', i['orgPrice'], i['sale'], i['cfav'], i['price'], i['similarityUrl'])
            info.insert_info(sql)
            print(flag, page)
        if flag:
            with open('page_number.txt', 'w', encoding='utf8') as f:
                f.write(str(page)+'spider over')
        page += 1
