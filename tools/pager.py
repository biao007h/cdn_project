
class Pagination(object):

    def __init__(self, dataCount, currentPage=1, cowCount=10, perPageCount=10):
        self.totalCount = dataCount
        self.perPageCount=perPageCount
        self.cowCount=cowCount
        if currentPage <= 0:
            self.currentPage=1
        elif currentPage>self.max_page:
            self.currentPage=self.max_page
        else:
            self.currentPage=currentPage
    @property
    def max_page(self):
        a,b=divmod(self.totalCount,self.perPageCount)
        if b==0:
            return a
        else:
            return a+1

    @property
    def start_page(self):
        # 1-10 2-11 3-12
        # 1-7 2-8 3-9
        # 假设当前页在中间，则有：
        step=int(self.cowCount/2)
        if self.currentPage<=step:
            return 1
        elif self.max_page-self.currentPage<step:
            return self.max_page-self.cowCount+1
        else:
            return self.currentPage-step+1

    @property
    def end_page(self):
        return self.start_page+self.cowCount-1
    @property
    # 模板语言的循环语句只有for in结构，只能返回列表供模板页面使用
    def page_range(self):
        return range(self.start_page, self.end_page+1)

    @property
    def next_page(self):
        if self.currentPage<self.max_page:
            return self.currentPage+1
        else:
            return "out"

    @property
    def prev_page(self):
        if self.currentPage > 1:
            return self.currentPage-1
        else:
            return "out"

    def data_start(self):
        return (self.currentPage-1)*self.perPageCount

    def data_end(self):
        return self.currentPage * self.perPageCount