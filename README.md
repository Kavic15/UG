#UG
Harmonogram:
  20.10•	Entity (UserGQLModel, MembershipGQLModel, GroupGQLModel, GroupTypeGQLModel)
  
  20.10•	Entity (RoleGQLModel, RoleTypeGQLModel, RoleCategoryGQLModel)
  
  27.10•	Modely v databázi pomocí SQLAlchemy, API endpoint typu GraphQL s pomocí knihovny Strawberry. 
  
  27.10•	Přístup k databázi řešte důsledně přes AioDataloder, resp. (https://github.com/hrbolek/uoishelpers/blob/main/uoishelpers/dataloaders.py). 
  
  5.11•	Zabezpečte kompletní CRUD operace nad entitami ExternalIdModel, ExternalIdTypeModel, ExternalIdCategoryModel 
  
  15.11•	CUD operace jako návratový typ nejméně se třemi prvky id, msg a „entityresult“ (pojmenujte adekvátně podle dotčené entity), vhodné přidat možnost nadřízené entity, speciálně pro operaci D.
  
  25.11•	Řešte autorizaci operací (permission classes).
  
  5.12•	Kompletní CRUD dotazy na GQL v souboru externalids_queries.json (dictionary), jméno klíče nechť vhodně identifikuje operaci, hodnota je dictionary s klíči query (obsahuje parametrický dotaz) nebo mutation (obsahuje parametrické mutation) a variables (obsahuje dictionary jako testovací hodnoty).
  
  15.12•	Kompletní popisy API v kódu (description u GQLModelů) a popisy DB vrstvy (comment u DBModelů).
  
  15.1•	Zabezpečte více jak 90% code test coverage (standard pytest).

  21.1• Uzavření projektu
  
Hodnocení:
  Absolvování jednoho projektového dne (součástí je commit na github ne starší než 1 týden) 5 b (x3, tj. 15 b), pod omluvě lze nahradit individuálně
  Příběh (na githubu) 5 b (součástí příběhu je časová posloupnost commitů, definice problémů k vyřešení)
  Řádné komentáře v kódu (včetně description u GQLModelů, strawberry fieldsa a comment u DBModelů) 5 b
  Vygenerovaná dokumentace 5 b
  Prokázaná funkčnost jako samostatný kontejner 5 b
  Prokázaná funkčnost jako prvek docker-compose (s odkazem na samostatný kontejner z docker hubu) 5 b
  Vytvoření docker containeru, publikace na Docker hub 5 b
  Kompletní CRUD 5 b_json 5 b
  Obhajoba 60 b, každý student předvede „dopracovaný“ SQL a GQL model (bez ohledu na týmovou práci)
  Lze získat až 120 bodů. Předmětem projdete, pokud budete mít více než 50 bodů, hodnocení „A“ získáte za 90 bodů a více
  

