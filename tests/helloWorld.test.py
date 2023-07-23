from example.wrappers.HelloWorld import contract_HelloWorld_class
priv_key = "657771027b21291cf102851b6a2b45c5393447786a729503b8416c8fc07b9cea" # do not use this in production
contract_obj = contract_HelloWorld_class(rpc="http://localhost:7545", private_key=priv_key)

# Call a function
print(contract_obj.execute_transaction_sayHello())