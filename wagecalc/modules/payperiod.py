import wagecalc.file
import gui

def main(self):
    self.mod_payperiod = gui.Module(self, "Pay Period Management")



# Not needed at the moment, already created a file with 200 pay periods in using this
#
# def create_pay_periods(self):
#     oneminute = timedelta(minutes=1)
#     oneday = timedelta(days=1)
#     fiveweeks = timedelta(weeks=5)
#     fourweeks = timedelta(weeks=4)
#     oneweek = timedelta(weeks=1)
#     self.all_pay_periods = []
#     answer = "y"
#     paydate = datetime.strptime('201109', '%d%m%y')
#     for i in range(200):
#         payfrom = (paydate - fiveweeks) + oneday
#         payto = (paydate - oneweek) + (oneday - oneminute)
#         payperiod = PayPeriod(self,paydate,payfrom,payto)
#         self.all_pay_periods.append(payperiod)
#         paydate = paydate + fourweeks
#
#     self.sbar.newtext(file.createpayperiods(self.all_pay_periods))
#     self.pay_window.destroy()




# payperiods = json.load([PayPeriod.__dict__ in PayPeriod], f)
