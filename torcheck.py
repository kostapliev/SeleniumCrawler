from ConnectionManager import ConnectionManager
# функция проверки работы тор
cm = ConnectionManager()
for j in range(5):
    for i in range(3):
        print (cm.request("http://icanhazip.com/").read())
    cm.new_identity()