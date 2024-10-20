# API Fitness

## Opis

API Fitness to backend stworzony w technologii Django Rest Framework, które obsługuje aplikację front-endową napisaną w React. Umożliwia autoryzację użytkowników przy użyciu JWT, a także zapewnia mechanizm automatycznego odświeżania tokenów. Dzięki temu użytkownicy mają dostęp do funkcji zarezerwowanych tylko dla zalogowanych. API zawiera również funkcje kalkulatora kalorii i generatora diety, które pozwalają użytkownikom na tworzenie spersonalizowanych planów dietetycznych i ich zapisywanie w bazie danych.

## Funkcje

- **Autoryzacja JWT**: Zastosowanie biblioteki `rest_framework_simplejwt` pozwala na wydawanie tokenów JWT, które umożliwiają bezpieczne logowanie użytkowników.
- **Automatyczny refresh tokena**: System automatycznie odświeża tokeny, co zapewnia nieprzerwaną sesję użytkownika i łatwy dostęp do zarezerwowanych funkcji.
- **Rejestracja i logowanie**: Umożliwienie użytkownikom zakupu konta oraz logowania się, co otwiera dostęp do aplikacji.
- **Kalkulator kalorii**: Użytkownicy mogą obliczać swoje dzienne zapotrzebowanie kaloryczne na podstawie wprowadzonych danych, takich jak wiek, płeć, waga i poziom aktywności fizycznej.
- **Generator diety**: API umożliwia generowanie spersonalizowanych planów dietetycznych, które można dostosować do preferencji żywieniowych użytkownika.
- **Zapis w bazie danych**: Użytkownicy mogą zapisywać swoje plany dietetyczne w bazie danych i uzyskiwać do nich dostęp za pośrednictwem API.

## Technologie

- **Django**: Użyte do stworzenia backendu.
- **Django Rest Framework**: Umożliwia łatwe tworzenie API.
- **PostgreSQL**: Użyty jako baza danych do przechowywania informacji o użytkownikach oraz planach dietetycznych.
- **rest_framework_simplejwt**: Umożliwia autoryzację JWT oraz automatyczne odświeżanie tokenów.
