# coding=utf-8


from main import log
import model
from config import key_state as default_key

def judge_phase(content,Express_Company):
    guess = []


    if default_key.get(Express_Company):
        key_state = default_key.get(Express_Company)
        # print(key_state,Express_Company)
    else:
        key_state = {
            '打包': '途中',
            '发出': '途中',
            '收入': '途中',
            '发往': '途中',
            '到达': '途中',
            '到件扫描': '揽件',
            '称重扫描': '途中',
            '进行分拨': '途中',
            '【反馈】扫描': '途中',
            '离开': '途中',
            '卸车扫描': '途中',
            '【称重】扫描': '途中',
            '【到件】扫描': '途中',
            '【卸车】扫描': '途中',
            '【分发】扫描': '途中',
            '快件扫描': '途中',
            '已拆包': '途中',
            '签收': '签收',
            '代收': '签收',
            '为您服务': '签收',
            '派件': '派件',
            '【派送】扫描': '派件',
            '收件': '揽收',
            '揽收': '揽收',
            '揽件': '揽收',
            '揽件扫描': '揽收',
            '问题件': '异常',
            '开始配送': '派件',
            '等待配送': '途中',
            '正在投递':'派件',
            '已收寄':'揽收',
            '接收':'途中',
        }

    for k, v in key_state.items():
        if k in content:
            guess.append(v)

    result = set(guess)
    situation = len(result)

    if situation == 1:
        # log.debug('成功=>' + content + '=>' + guess[0])
        return (1, guess[0])

    if situation > 1:
        if '问题件' in guess:
            log.debug('歧义=>' + content + '=>' + '问题件')
            return (1, '异常')
        if '已揽件' in content or '已揽收' in content:
            log.debug('歧义=>' + content + '=>' + '揽收')
            return (1, '揽收')
        if '已签收' in content or '签收人' in content:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')
        if '代收' in content and '取件' in content:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')
        if '途中' in guess and '收件' in guess:
            log.debug('歧义=>' + content + '=>' + '途中')
            return (1, '途中')
        if '途中' in guess and '签收' in guess:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')
        if '已被' in guess and '代签收' in content:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')
        if '派件' in content and '代收' in content:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')

        if '进行扫描' in content:
            log.debug('歧义=>' + content + '=>' + '途中')
            return (1, '途中')

        if '派件' in content:
            log.debug('歧义=>' + content + '=>' + '派件')
            return (1, '派件')


        log.debug('歧义=>分析失败=>' + content + '=>' + ','.join(result))

        # 关键字优先级
        key_sort = ['签收','揽收','派件','异常','途中']
        for i in key_sort:
            if i in guess:
                return (1, i)
        return (1, guess[0])
    if situation == 0:

        if '快件异常' in content:
            log.debug('歧义=>' + content + '=>' + '异常')
            return (1, '异常')


        log.debug('失败=>' + content)
        return (0, content)


def manual_check_judge_phase(type):
    """
    手动更新状态
    :param type:全部更新或只更新未知部分
    :return:
    """
    pass
    # db = model.Express_by_MS()
