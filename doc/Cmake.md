# documentatie van research voor Cmake

## cmake

CMake is cross platform voor build automation in c++/c, kan ook in een andere taal, maar is niet vaak  
Genereerd platform specifiek build files  
Ontwikkelaars schrijven CmakeLists.txt files, waarin wordt beschreven hoe de structuur eruit ziet van het project, de dependencies en de build config  
Kan voor verschillende systemen gemaakt worden  

Beter voor verschillende platformen en build environments, higher level platform-specific

## make

Een build automation dat de compilatie van scource code in exe programs of libraries beheert  
Het leest de MakeFile wat de regels en de dependencies voor het builden bezit  

Lower level, gebasseerd op de regels en commando's in de MakeFile

## Verschil

Cmake maakt de Make file van de source code, Make maakt executables van de Make file gamaakt door Cmake