# Operator overloading

## Mik az operátorok valójában?

Az operátorok valójában csak speciális függvények. Ez azt jelenti, hogy ugyanúgy bánhatunk velük, habár van némi megkötés, azonban legtöbbször ezek nem fognak az utunkban állni. 

## Operátorok és osztályok

Ha egy operátor az adott osztály típust veszi át baloldali paraméterként (vagy unáris, egyparaméterű operátor), akkor az operátort az osztályon belül tagfüggvényként kezelhetjük. Ekkor valójában egy paramétert adunk neki, ami a jobb oldali operandus. A bal oldali operandusa implicit a `this` pointer lesz.

Szeretnénk, hogy a tömbünkhöz a += operátorral is lehessen új elemet hozzáadni. Ehhez túl kell töltenünk += operátort.
A += operátorra "függvényként" az `operator+=` kifejezéssel hivatkozhatunk.

Nézzünk egy példát:

```cpp
class DinTomb{
    /* 
        ...
    */

    void operator+=(const T& elem){
        push_back(elem); //delegáljuk a beillesztést a push_back függvénynek, nem duplikálunk kódot.
    }
};

int main(){
    DinTomb tomb;
    tomb += 5.2; // értelmezzük: tomb.operator+=(5.2) -> operator+=(&tomb, 5.2)

    return 0;
}
```

## Friend

Most szeretnénk, ha a tömbünket ki is lehetne írni. Viszont ezzel van egy kis gond. Azt, hogy hova írjuk ki a tömböt(stdout, file, stb.) balértékként veszi át az `operator<<` (stream insertion operator), ezért ezt az osztályon kívük kell túltölteni. 
A `friend` kulcsszó használatával az osztályon belül deklaráljuk a függvényt, ezzel "megengedjuk" neki, hogy a privát tagokat is lássa. Eztunán az osztályon kívül definiáljuk.

```cpp
#include <iostream>

class DinTomb{
    /* 
        ...
    */

    template<typename K>
    friend std::ostream& operator<<(std::ostream& out, const DinTomb<K>& dtomb);
};

template<typename K>
std::ostream& operator<<(std::ostream& out, const DinTomb<K>& dtomb){
    for(std::size_t i = 0; i < dtomb.meret; ++i){
        out << dtomb.tomb[i] << ' ';
    }

    return out;
}

int main(){
    DinTomb tomb;
    tomb += 5.2; // értelmezzük: tomb.operator+=(5.2) -> operator+=(&tomb, 5.2)
    tomb += 2.3;
    tomb.push_back(8.7);

    std::cout << tomb; //értsd: operator<<(std::cout, tomb);
    return 0;
}
```
Ha az `operator<<`-t streamre való kiírásra használjuk, akkor mindig `std::ostream&` -et ad vissza és vesz át bal operandusként, valamint visszaadja a bal operandusát, így láncolhatóvá teszi az operátort. (`std::cout << a << b << c;`)

Természetesen ezt a példát `friend` nélkül is meg lehet oldani, azonban ez nem mindig van így.

## Copy assignment(értékadó operátor)

Vannak olyan esetek, amikor már egy kész objektumnak akarunk új értéket adni. 
Pl.

```cpp
tomb<int> tomb1;
tomb1.push_back(5);

tomb<int> tomb2;
tomb2.push_back(1);

tomb1 = tomb2;
```

Ilyen esetekben egy értékadó operátor(copy assignment operator) hívásról beszélünk.

A másoló konstruktor testvére a copy assignment(értékadó) operator. A copy constructorhoz hasonlóan `const T&` -ként veszi át a másolandó objektumot és a default is generálódik belőle.
Fontos, hogy a copy assignment operátor nem új objektumot hoz létre így az előzőleg használt erőforrásokat fel kell szabadítani.

```cpp
template <typename T>
class DinTomb{
    T* tomb;
    std::size_t meret;

public:
    /**
     * @brief Default konstruktor, mindent 0-ra inicializál
     */
    DinTomb() : tomb(nullptr), meret(0) {}


    /**
     * @brief Másoló konstruktor
     * @param other a másik tömb amit másolunk
     */
    DinTomb(const DinTomb& other) : tomb(other.tomb != nullptr ? new T[other.meret] : nullptr), meret(other.meret) {
        //                                          ^ ha nullptr a másik tömb(vagy 0 a mérete), akkor nem foglalunk 0 méretű tömböt(nem is lehetne...)
        for(std::size_t i = 0; i < other.meret; ++i){
            tomb[i] = other.tomb[i];
        }
    }

    /**
     * @brief Értékadó operátor
     * @param other a másik tömb amit másolunk
     * @return referencia a tömbre aminek értéket adtunk
     */
    DinTomb& operator=(const DinTomb& other){
        if(this == &other) { //ha önmagát kapja paraméterül akkor nincs semmi teendő, ne vágjuk magunk alatt a fát
            return *this; // *this -> this pointer, *this referencia(az objektumra amin a hívás történt)
        }
        delete[] tomb;
        tomb = new T[other.meret];
        meret = other.meret;
        for(std::size_t i = 0; i < other.meret; ++i) {
            tomb[i] = other.tomb[i];
        }
        return *this;
    }

    ~DinTomb() {
        delete[] tomb;
    }

    std::size_t size() const;

    void push_back(const T& elem);

    T& at(std::size_t idx);

    T& at(std::size_t idx) const;
};

int main(){

}
```

## Rule of 0/3

<https://en.cppreference.com/w/cpp/language/rule_of_three>

Rule of 3: Ha egy osztálynak szüksége van nem compiler-default destruktorra, másoló konstruktorra vagy copy assignment operátorra akkor majdnem biztosan szüksége van mindháromra.

__*advanced*__<br>
Rule of 0: Azok az osztályok, amelyeknek nem compiler-default destructora, copy constructora, copy assignment operátora van, azok valamilyen explicit erőforrás-birtoklást valósítanak meg. (<https://en.cppreference.com/w/cpp/language/rule_of_three>). Ettől eltérő osztályoknak ne legyen nem compiler-default destruktora, copy constructora vagy copy assignment operátora.

## Néhány kötöttség

Operátor túltöltéssel nem változtatható meg:
* precedencia
* asszocivitás

Ezen felül egyes operátoroknak csak kötött számú paramétere lehet.<br>
A logikai(`||` és `&&`) operátorok túltöltése esetén azok elvesztik a short-circuit tulajdonságukat.

## Összehasonlító operátorok

Természetesen mindenféle más operátorokat, pl összehasonlító, ennek negáltja, nagyobb, kisebb, stb. is overloadolhatunk. 

Pl. a tömbjeink összehasonlítása:

```cpp
template <typename T>
class DinTomb{
    T* tomb; //pointer a dinamikus tömbre
    std::size_t meret; //a dinamikus tömb mérete

public:
    //...

    bool operator==(const DinTomb& other) {
        if(meret != other.meret) {
            return false;
        }

        for(std::size_t i = 0; i < meret; ++i) {
            if(tomb[i] != other.tomb[i]) {
                return false;
            }
        }

        return true;
    }

    bool operator !=(const DinTomb& other) {
        return !(*this == other);
    }
};

```

Pl. indexelő operátor:

```cpp
template <typename T>
class DinTomb{
    T* tomb; //pointer a dinamikus tömbre
    std::size_t meret; //a dinamikus tömb mérete

public:
    //...

    T& at(std::size_t idx);

    const T& at(std::size_t idx);

    T& operator[](std::size_t idx){
        return at(idx); //delegáljuk a feladatot a már implementált at() tagfüggvénynek
    }

    const T& operator[](std::size_t idx) const{
        return at(idx);
    }
};
```