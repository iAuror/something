from django.shortcuts import render
from django.views import View


class Shop(View):
    def shop(self,request):
        context={'title':'Shop Book',
                 'name':['Egor','Oleg','Anton']
                 }
        return render(request,'manager/index.html',context=context)
