from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bank_database import Base,Bank,Teller,Customer,Transactions,Card_Application,Loan

#lets the program know which database its going to be working with
engine = create_engine('sqlite:///bank.db')

#t#this binds the base class to the engine class
Base.metadata.bind = engine
#session maker object establishes a link between our code executions and out database
DBsessions = sessionmaker(bind=engine)

session = DBsessions()
# session.add is to add stuff to database, session.commit is to enable a change in the database
# session.query checks if an item exist in the database

class bank:
    def register_bank(self, bankname, banklocation):
        bank1 = Bank(bank_name=bankname ,bank_location = banklocation)
        session.add(bank1)
        session.commit()

    def all_banks(self):
        banks = session.query(Bank).all()
        for bank in banks:
            #print(bank.date)
            print(bank.bank_id)
            print(bank.bank_name)
            print(bank.bank_location)
            print('\n')

    def add_teller(self,tellername,bankID):
        teller = Teller(teller_name = tellername,teller_id=bankID)
        session.add(teller)
        session.commit()

    def all_tellers(self):
        teller = session.query(Teller).all()
        for tel in teller:
            print(tel.id)
            print(tel.teller_name)
            print(tel.teller_id)
            print('\n')

    def all_customers(self):
        custs = session.query(Customer).all()
        for  cust in custs:
            print(cust.account_number)
            print(cust.account_name)
            print(cust.account_type)
            print('\n')

class transactions:

    def transactions_conducted(self):
        transact = session.query(Transactions).all()
        for trans in transact:
            print(trans.customer_name)
            print(trans.account_number)
            print(trans.type_trans)
            print(trans.amount)
            print(trans.teller_id)
            print("\n")

    def transactionBy_teller(self,tellerID):
        transact = session.query(Transactions).filter_by(teller_id=tellerID).all()
        for trans in transact:
            print(trans.customer_name)
            print(trans.account_number)
            print(trans.type_trans)
            print(trans.amount)
            print("\n")

    def transaction4_customer(self,accountNumber):
        transact = session.query(Transactions).filter_by(account_number=accountNumber).all()
        for trans in transact:
            print(trans.customer_name)
            print(trans.account_number)
            print(trans.type_trans)
            print(trans.amount)
            print(trans.teller_id)
            print("\n")

class tellerD:
    def OpenAccount(self,cname,phoneN,accType,amountDepo,tellerID):
        custm = Customer(account_name=cname, phone_number=phoneN, account_type = accType, balance=amountDepo)
        session.add(custm)
        session.commit()
        accID=session.query(Customer).filter_by(phone_number=phoneN).first()
        trans = Transactions(type_trans="creating account", account_number=accID.account_number, amount=amountDepo, teller_id=tellerID)
        session.add(trans)
        session.commit()
        card = Card_Application(account_number=accID.account_number,account_name=cname,reason_for="NEW ACCOUNT")
        session.add(card)
        session.commit()
        print("ACCOUNT CREATED")

    def CollectMoney(self,accNum,amount,tellerID):
        accs = session.query(Customer).filter_by(account_number=accNum).all()
        for acc in accs:
            print(acc.account_name)
            print("previous balance --> %s" % acc.balance)
            print(acc.loan)
            print("\n")
        acs = session.query(Customer).filter_by(account_number=accNum).one()
        X = acs.balance + amount
        acs.balance = X
        session.add(acs)
        session.commit()
        print(acs.balance)
        print("\n")
        trans = Transactions(type_trans="DEPOSITE", account_number=acs.account_number, amount=amount, teller_id=tellerID)
        session.add(trans)
        session.commit()

    def loan_repayment(self,loanID,amount,tellerID):
        debts = session.query(Loan).filter_by(loan_id=loanID).one()
        print(debts.amount)
        w = debts.amount-amount
        debts.amount = w
        session.add(debts)
        session.commit()
        print(debts.amount)
        print("SUCCESSFUL")
        print("\n")
        trans = Transactions(type_trans="LOAN REPAYMENT", account_number=loanID, amount=amount, teller_id=tellerID)
        session.add(trans)
        session.commit()

    def closeAccount(self,accNumb):
        acc = session.query(Customer).filter_by(account_number=accNumb).one()
        print(acc.account_name)
        session.delete(acc)
        session.commit()
        print("successfull")

    def ProvidInfo(self,accNu):
        accNs = session.query(Customer).filter_by(account_number=accNu)
        for accN in accNs:
            print("account number --> %s" % accN.account_number)
            print("account name --> %s" % accN.account_name)
            print("account balace --> %s" % accN.balance)
            print("loan --> %s" % accN.loan)
            print("\n")

    def issueCard(self,cardNumber):
        cards = session.query(Card_Application).filter_by(card_number=cardNumber).one()
        cards.issued_card = 'ISSUED'
        session.add(cards)
        session.commit()
        print(cards.issued_card)

    def allCards(self):
        cards = session.query(Card_Application).all()
        for card in cards:
            print(card.card_number)
            print(card.account_number)
            print(card.account_name)
            print('\n')

class account():
    def check(self,accountNumber):
        accs = session.query(Customer).filter_by(account_number=accountNumber).one()
        print(accs.account_type)

class customer():
    def Generalinquiry(self,name,phoneNumber):
        genInqs = session.query(Customer).filter_by(account_name=name).all()
        for genInq in genInqs:
            print(genInq.account_number)
            print(genInq.account_name)
            print(genInq.balance)
            print(genInq.loan)
        GenInqs = session.query(Customer).filter_by(phone_number=phoneNumber).all()
        for GenInq in GenInqs:
            print(GenInq.account_number)
            print(GenInq.account_name)
            print(GenInq.balance)
            print(GenInq.loan)

    def DepositMoney(self,accNum,amount,tellerID):
        acs = session.query(Customer).filter_by(account_number=accNum).one()
        print(acs.balance)
        X = int(input('ADD DEPOSIT PLUS BALANCE AND ENTER THE NEW BALANCE'))
        acs.balance = X
        session.add(acs)
        session.commit()
        print(acs.balance)
        print("\n")
        trans = Transactions(type_trans="DEPOSITE BY CUSTOMER", account_number=acs.account_number, amount=amount, teller_id=tellerID)
        session.add(trans)
        session.commit()

    def withDrawMoney(self,accountNumber,amount,tellerID):
        acs = session.query(Customer).filter_by(account_number=accountNumber).one()
        if acs.balance < amount:
            print("YOUR BALANCE IS INSUFFICIENT FOR THIS TRANSACTION")

        else:
            cash = acs.balance - amount
            acs.balance = cash
            session.add(acs)
            session.commit()
            print(acs.balance)
            print("\n")
            trans = Transactions(type_trans="WITHDRAW BY CUSTOMER", account_number=accountNumber, amount=amount, teller_id=tellerID)
            session.add(trans)
            session.commit()

    def ApplyForLoan(self,name,security,pay_date,cash):
        loan = Loan(account_name=name,Security=security,amount=cash,date_pay=pay_date)
        session.add(loan)
        session.commit()
        print("SUCCESSFUL")


    def RequestCard(self,acc_name,acc_number,reason):
        OldCard = session.query(Card_Application).filter_by(account_number=acc_number).one()
        session.delete(OldCard)
        session.commit()
        NewCard = Card_Application(account_number=acc_number,account_name=acc_name,reason_for=reason)
        session.add(NewCard)
        session.commit()
        print("SUCCESSFUL")

