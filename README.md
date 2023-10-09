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

