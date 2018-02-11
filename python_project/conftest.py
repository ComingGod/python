import pytest
class hah(object):
    def __init__(self):
        self.a = 'aaa'
        self.b = 'bbb'
    def output(self,argument):
        print '==================='
        print self.a
        print self.b
        print argument
         
def dd():
    hah = test()
    return hah
@pytest.fixture(scope = 'function')
def bl(request):
    BL = hah()
    return BL
    

# if __name__ == '__main__':
#     a = dd()
#     print 'dd'
#     a.output()
        
        