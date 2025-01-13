# Kivételek, hibakezelés

## Hibakezelés C-ben

```c

double oszt(double x, double y){
    if(y == 0){
        //mit csináljunk? exit, vagy csak írjunk ki valamit? 
    }else{
        return x/y;
    }
}
```

## C++ -ban
<https://en.cppreference.com/w/cpp/language/exceptions>

A C++ egy fontos nyelvi elemei a kivételek(exception). Ezek segítségével *kivétel*es esetekkor dobhatunk egy "hibát", amit a program elkaphat. Ez egy megosztó feature a közösségben(ld. "hidden control flow"), viszont sokszor hasznos lehet. Például nullával való osztás esetén valószínűleg nem nekünk, hanem a hívó kódnak kéne kezelnie a hibát.

Kivételt a `throw` kulcsszóval dobhatunk, valamint a `try` kulcsszóval nyitott scope-ban dobott kivételeket a `catch` kulcsszóval kaphatunk el.

Kivételként bármilyen típust dobhatunk(int, const char*, stb.), viszont érdemes az `std::exception` és a belőle leszármazó(később) típusú objekutmokat dobni. Ezekhez az `stdexcept` nevű header-re van szükség.

<https://en.cppreference.com/w/cpp/error/exception>


```cpp
double oszt(double x, double y){
    if(y == 0){
        throw std::runitme_error("0-val valo osztas!"); 
        /*
        lehetne:
        throw "0-val valo osztas";
        vagy
        throw 0;
        stb. viszont ezeket nem szép dobni.
        */
    }else{
        return x/y;
    }
}

int main(){
    try{
        oszt(5.0, 0.0);
    }catch(std::exception& e){ //referenciaként kapjuk el az exception-t
        std::cout << e.what(); //.what() : visszaadja az exception "üzenetét"
        //egyéb hibakezelő kód...
    }
}
```

Később lesz szó arról, hogy hogyan készíthetünk saját kivétel típusokat amelyek az `std::exception` -ből származnak.