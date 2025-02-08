# Iterátorok

Most elengedjük egy kicsit a tömböket, és megnézünk egy láncolt lisát.

```cpp
template <typename T>
class List{
    struct node{ //belső osztály, List<T>::node
        T data;
        node* next;
    };

    node* m_head;
    node* m_back;
    std::size_t m_size;

public:
    List() : m_head{nullptr}, m_back(nullptr), m_size(0) {}

    List(const List& other) : m_head(nullptr), m_back(nullptr), m_size(0) {
        for(const auto& elem : other) {
            push_back(elem);
        }
    }

    ~List() {
        node* iter = m_head;
        while (iter != nullptr) {
            node* tmp = iter;
            iter = iter->next;
            delete tmp;
        }
    }

    void push_front(T data) {
        node* uj = new node;
        uj->data = data;
        uj->next = m_head;
        if(m_size == 0) {
            m_back = uj;
            m_head = uj;
        }else {
            m_head = uj;
        }
        ++m_size;
    }

    void push_back(const T& data) {
        if(m_size == 0) {
            push_front(data);
            return;
        }else {
            node* uj = new node;
            uj->data = data;
            uj->next = nullptr;
            m_back->next = uj;
            m_back = m_back -> next;
        }
        ++m_size;
    }

    std::size_t size() const {
        return m_size;
    }
};
```

Ha ezen a listán végig szeretnénk iterálni, akkor az valamilyen ronda `->next` és `==nullptr` -el teli kódot eredményezne.

Ehelyett készíthetünk egy segédosztályt, amely az iterálás lépéseit absztraktálja el. Az ilyen osztályokat nevezzük iterátornak.
Ahhoz, hogy egy iterátor használható legyen legalább szükség van valamilyen léptető operátorra, dereferencia operátorokra, valamint összehasonlító(== != stb.) operátorokra is.

Pl.:

<https://godbolt.org/z/qchjxE9en>
```cpp
template <typename T>
class List{
    struct node{
        T data;
        node* next;
    };

public:
    struct iterator{
        friend class List; 
    private:
        node* it; //az iterátor egy pointer absztrakció, azt tárolja hogy éppen melyik node-ra mutat
        explicit iterator(node* it) : it(it) {} //privát konstruktor, nem kell hogy a hívó fél manuálisan csináljon iterátorokat
    public:
        iterator(const iterator& other) : it(other.it) {}
        
        iterator& operator= (const iterator& other) {
            it = other.it;
            return *this;
        }

        /**
         * @brief léptető preincrement operátor, a current = current->next műveletet absztraktálja
         * @return
         */
        iterator& operator++() {
            it = it->next;
            return *this;
        }

        /**
         * @brief összehasonlító operátor FONTOS!
         * @param other
         * @return
         */
        bool operator==(const iterator& other) const {
            return it == other.it;
        }

        /**
         * @brief összehasonlító operátor FONTOS(talán a legfontosabb)
         * @param other
         * @return
         */
        bool operator!=(const iterator& other) const {
            return  !(it == other.it);
        }

        /**
         * @brief dereferencia operátor
         * @return
         */
        T& operator*() {
            return it->data;
        }

        /**
         * @brief konstans dereferencia operátor
         * @return
         */
        const T& operator*() const {
            return it->data;
        }

        /**
         * @brief nyíl operátor ha az iterátoron keresztül közvetlen egy osztály tagjait akarjuk elérni
         * @return
         */
        T* operator->() {
            return &(it->data);
        }

        //ugyanaz mint a másik, csak konstans
        T* operator->() const {
            return &(it->data);
        }
    };

private:
    node* m_head; //lista első eleme
    node* m_back; //lista utolsó, még érvényes eleme
    std::size_t m_size; //lista mérete

public:
    List() : m_head{nullptr}, m_back(nullptr), m_size(0) {}

    List(const List& other) : m_head(nullptr), m_back(nullptr), m_size(0) {
        for(const auto& elem : other) {
            push_back(elem);
        }
    }

    ~List();

    void push_front(T data);

    void push_back(const T& data);

    std::size_t size() const;

    /**
     * @brief begin tagfüggvény az iteráláshoz
     * @return az első elemre mutató iterátor
     */
    iterator begin() {
        return iterator(m_head);
    }

    // Minden iterátort visszaadó tagfüggvényből készül konstans verzió is ami konstans iterátort ad vissza.
    const iterator begin() const {
        return iterator(m_head);
    }

    /**
     * @brief end tagfüggvény az iteráláshoz
     * @return az utolsó érvényes elem "után" mutató iterátor, "sentinel" iterátor
     */
    iterator end() {
        return m_back == nullptr ? iterator(m_back) : iterator(m_back->next);
    }
    
    const iterator end() const {
        return m_back == nullptr ? iterator(m_back) : iterator(m_back->next);
    }
};

int main(){
    List<int> list;

    for(int i = -3; i < 5; ++i){
        list.push_back(i);
    }

    for(List<int>::iterator it = list.begin(); it != list.end(); ++it) {
        std::cout << *it << ' ';
    }

    std::cout << '\n';
    *list.begin() = 5;

    for(int elem : list) { //minden elemet lemásolunk egyesével
        std::cout << elem << ' ';
    }
}
```

A fent látott

```cpp
for(List<int>::iterator it = list.begin(); it != list.end(); ++it) {
        std::cout << *it << ' ';
}
```
kódrészlet olyan gyakori, hogy külön szintaxis létezik rá:

```cpp
for(int elem : list) { //minden elemet lemásolunk egyesével
        std::cout << elem << ' ';
}

for(int& elem : list) { //minden elemre referenciával hivatkozunk
        std::cout << elem << ' ';
}

for(const int& elem : list) { //ua. mint az előbb, csak konstans referenciával
        std::cout << elem << ' ';
}
```

Gondoljunk az iterátorokra úgy, mint a felturbózott pointerekre. Minden iterátor valamilyen tárolóhoz igazított, speciális mutató típus.

A következő fejezetben azt láthatjuk, hogy valójában a pointerek a tömb féle tárolók iterátorai.

## Iterátorok, tömbök és pointerek

A pointerek kielégítik az iterátorok legmélyebb követelményét, a [*LegacyRandomAccessIterator*](https://en.cppreference.com/w/cpp/named_req/RandomAccessIterator) követelményt. 
Ez azt jelenti, hogy egy dinamikus tömbnél például nincs szükség külön iterátor osztályra, hiszen elég a pointereket léptetni és összehasonlítani.

Ez azt jelenti, hogy egy dinamikus tömböt elég ennyivel kiegészíteni:
```cpp
    T* begin() {
        return tomb;
    }

    const T* begin() const {
        return tomb;
    }

    T* end() {
        return tomb + meret;
    }

    const T* end() const {
        return tomb + meret;
    }
```