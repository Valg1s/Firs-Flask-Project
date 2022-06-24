from sweter import db

from sweter.models import Medicines, Manufacturer, Category, Pharmacy


def add_manuf():
     rekkit = Manufacturer(title_of_man =' Реккітт Бенкізер Хелскер' ,
    country = 'Велика Британія')
     beringer = Manufacturer(title_of_man =' Берінгер Інгельхайм Еллас' ,
    country = 'Греція')
     dar =  Manufacturer(title_of_man =' ФФ Дарниця' ,
    country = 'Україна')
     farmak = Manufacturer(title_of_man =' ФФ Фармак' ,
    country = 'Україна')
     orisil = Manufacturer(title_of_man =' Орісіл-Фарм' ,
    country = 'Україна')
     lek_him = Manufacturer(title_of_man =' Лекхім-Харків' ,
    country = 'Україна')

     db.session.add(rekkit)
     db.session.add(beringer)
     db.session.add(dar)
     db.session.add(farmak)
     db.session.add(orisil)
     db.session.add(lek_him)

     db.session.commit()
     db.session.close()

def add_cat():
    hot_down = Category(name_of_cat = 'Жарознижувальне')
    muk = Category(name_of_cat = 'Муколітичний')
    diareya = Category(name_of_cat = 'Антидіарейні припарати(Єнтеросорбент)')

    db.session.add(hot_down)
    db.session.add(muk)
    db.session.add(diareya)

    db.session.commit()
    db.session.close()

def add_med():
    nurofen = Medicines(med_name = 'Nurofen Forte',
                        med_count = 100 ,
                        form_of_production = 'Таблетки' ,
                        id_of_manufacturer = 1 ,
                        cost = 110 ,
                        category =  1,
                        active_substance = 'Ібупрофен',
                        volume_of_active_substance = 400 ,
                        volume = 12,
                        name_of_picture ="NurofenForte.png")

    lazolvan = Medicines(med_name='Лазолван',
                        med_count=100,
                        form_of_production='Таблетки',
                        id_of_manufacturer=2,
                        cost=85,
                        category=2,
                        active_substance='Амброксол хідрохлорид',
                        volume_of_active_substance= 30,
                        volume=20,
                         name_of_picture ="Лазолван.png")
    brom = Medicines(med_name='Бромгексин - Дарниця',
                         med_count=100,
                         form_of_production='Таблетки',
                         id_of_manufacturer=3,
                         cost=40,
                         category=2,
                         active_substance='Бромгексин хідрохлорид',
                         volume_of_active_substance=8,
                         volume=50,
                     name_of_picture ="Бромгексин.png")
    apsorb = Medicines(med_name='Абсорбін Саше',
                        med_count=100,
                        form_of_production='Порошок в пакетику',
                        id_of_manufacturer=4,
                        cost=140,
                        category=3,
                        active_substance='Діосимектит',
                        volume_of_active_substance=300,
                        volume=10,
                       name_of_picture ="Абсорбін.png")
    atox = Medicines(med_name='Атоксіл Гель',
                        med_count=100,
                        form_of_production='Гель в стіках',
                        id_of_manufacturer=5,
                        cost=140,
                        category=3,
                        active_substance='Діоксид кремнію високодисперсний',
                        volume_of_active_substance= 160 ,
                        volume=20,
                     name_of_picture = "Атоксіл.png")
    loper = Medicines(med_name='Лоперамід',
                        med_count=100,
                        form_of_production='Таблетки',
                        id_of_manufacturer=6,
                        cost=16,
                        category=3,
                        active_substance='Лоперамід',
                        volume_of_active_substance=20,
                        volume=12,
                      name_of_picture ="Лоперамідю.png")

    db.session.add(nurofen)
    db.session.add(lazolvan)
    db.session.add(brom)
    db.session.add(apsorb)
    db.session.add(atox)
    db.session.add(loper)

    db.session.commit()
    db.session.close()

def add_phar():
    phar1 = Pharmacy(
    adress_of_phar = "Пр.Гагаріна 193а",
    number_of_phar = 1
    )
    phar2 = Pharmacy(
        adress_of_phar="Пр.Гагаріна 10",
        number_of_phar=2
    )
    phar3 = Pharmacy(
        adress_of_phar="Пр.Героїв Харкова 25",
        number_of_phar=3
    )

    db.session.add(phar1)
    db.session.add(phar2)
    db.session.add(phar3)

    db.session.commit()
    db.session.close()

if __name__ == "__main__":
    print("Insert Manufacturers...")
    add_manuf()
    print("Ready, insert Categories")
    add_cat()
    print('Ready, insert Medicines')
    add_med()
    print('Ready, insert Pharmacy')
    add_phar()
    print('Insert finished')