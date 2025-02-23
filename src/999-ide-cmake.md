# CMake

A CMake egy meta-build system. Ez azt jelenti, hogy önmagában nem funkcionális, szükség van mellé egy C++ compilerre (pl. MSVC, g++, stb.) és egy build systemre is. Emellé szükség lesz még egy build systemre. Egy egyszerű de nagyon gyors build system a [Ninja](https://github.com/ninja-build/ninja/releases).

A CMake előnye, hogy operációs rendszertől és fordítótól függetlenül működik.

### Miért pont CMake?

A VS Code beépített task rendszere elég janky egy normális build system nélkül, a CLion pedig kb. csak a CMake projekteket képes értelmesen kezelni.

## CMake alapok

A `CMakeLists.txt` file írja le a projekt buildelését. Gondolhatunk rá úgy, mint a "script"re.

```cmake
cmake_minimum_required(VERSION 3.25) #megadunk egy cmake verziót amire minimum szükség lesz

project(prog2) #csinálunk egy projektet

set(CMAKE_CXX_STANDARD 11) # a set() függvénnyel változóknak adhatunk értéket.


#az add_executable függvényben megadunk konkrét futtatható végeredményeket, mellette felsoroljuk a hozzá tartozó forrásfájlokat
add_executable(labor1 fuggvenyeim.h fuggvenyeim.cpp)

#egy projekthez több executable is tartozhat
add_executable(labor1_test test.cpp)
```
