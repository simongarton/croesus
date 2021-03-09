-- Bills

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Power', '{"column":"payee","operation":"equals","value":"MERCURY NZ LTD"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Water', '{"column":"payee","operation":"equals","value":"WATERCARE SERVICES"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Phone & BB', '{"column":"payee","operation":"equals","value":"VODAFONE FIXED"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Mobile', '{"column":"payee","operation":"equals","value":"Vodafone Ptpy Vcc Vm R Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Rates', '{"column":"payee","operation":"equals","value":"Z AUCKLAND CITY RATE"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Bank fees', '{"column":"payee","operation":"equals","value":"GROUP FEE WAIVER"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Bank fees', '{"column":"payee","operation":"equals","value":"Monthly A/C Fee"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Bank Interest', '{"column":"transaction_type","operation":"equals","value":"INT"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Pets', '{"column":"payee","operation":"equals","value":"Animates Three Kings   Three Kings   Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Pets', '{"column":"payee","operation":"equals","value":"Ellerslie Vet Clinic   Ellerslie     Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Pets', '{"column":"payee","operation":"equals","value":"Hollywood Fish Farm    Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Bills', 'Kids phones', '{"column":"payee","operation":"equals","value":"Spark Prepaid          0800323232    Nzl"}');

-- Groceries

INSERT INTO category (category, sub_category, rules)
VALUES ('Groceries', 'Countdown', '{"column":"payee","operation":"equals","value":"COUNTDOWN GREENLANE"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Groceries', 'Countdown', '{"column":"payee","operation":"contains","value":"Countdown"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Groceries', 'PakNSave', '{"column":"payee","operation":"contains","value":"Pak N Save"}');

-- Insurance

INSERT INTO category (category, sub_category, rules)
VALUES ('Insurance', 'State', '{"column":"payee","operation":"equals","value":"STATE INSURANCE"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Insurance', 'State', '{"column":"payee","operation":"equals","value":"IAG NEW ZEALAND"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Insurance', 'Health', '{"column":"payee","operation":"equals","value":"NIB NZ LTD"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Insurance', 'Life', '{"column":"payee","operation":"equals","value":"AIA NZ"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Mortgage', 'Home', '{"column":"payee","operation":"equals","value":"GARTON&MARTINEZ"}');

-- Media

INSERT INTO category (category, sub_category, rules)
VALUES ('Media', 'Amazon', '{"column":"payee","operation":"equals","value":"Amazon Video           Amazon.Com    Wa"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Media', 'Apple', '{"column":"payee","operation":"equals","value":"Apple Nz Gcs           Sydney        Au"}');
INSERT INTO category (category, sub_category, rules)
VALUES ('Media', 'Apple', '{"column":"payee","operation":"equals","value":"Apple.Com/Bill         Sydney        Au"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Media', 'Disney', '{"column":"payee","operation":"equals","value":"Disney Plus            Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Media', 'Neon', '{"column":"payee","operation":"equals","value":"Neon                   Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Media', 'Netflix', '{"column":"payee","operation":"contains","value":"Netflix"}');

-- Transfers

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Jake - long term saving', '{"column":"other_account","operation":"equals","value":"02-0256-0011141-66"}');
INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Jake - pocket', '{"column":"other_account","operation":"equals","value":"02-0256-0011141-67"}');
INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Jake - spending', '{"column":"other_account","operation":"equals","value":"02-0256-0011141-83"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Sam - long term saving', '{"column":"other_account","operation":"equals","value":"02-0256-0011184-66"}');
INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Sam - pocket', '{"column":"other_account","operation":"equals","value":"02-0256-0011184-67"}');
INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Sam - spending', '{"column":"other_account","operation":"equals","value":"02-0256-0011184-83"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Maddy - long term saving', '{"column":"other_account","operation":"equals","value":"02-0256-0011192-66"}');
INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Maddy - pocket', '{"column":"other_account","operation":"equals","value":"02-0256-0011192-67"}');
INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Maddy - spending', '{"column":"other_account","operation":"equals","value":"02-0256-0011192-83"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Supermarket', '{"column":"other_account","operation":"equals","value":"02-0200-0299561-03"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Helen - shares', '{"column":"other_account","operation":"equals","value":"01-1841-0136396-46"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Helen - BNZ', '{"column":"other_account","operation":"equals","value":"02-0256-0028330-00"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Schools account', '{"column":"other_account","operation":"equals","value":"02-0200-0299561-02"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Simon - income', '{"column":"other_account","operation":"equals","value":"02-0256-0061720-01"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Simon - work', '{"column":"other_account","operation":"equals","value":"02-0256-0061720-83"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Simon - ANZ', '{"column":"other_account","operation":"equals","value":"06-0287-0322436-00"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Simon - BNZ', '{"column":"payee","operation":"equals","value":"Garton Sh"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Online', '{"column":"payee","operation":"equals","value":"Online       Payment -  Thank You"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Transfer', 'Simon - BNZ', '{"column":"payee","operation":"equals","value":"Bnz Joint Account"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Transferwise', '{"column":"payee","operation":"contains","value":"Transferwise"}');

-- Miscellaneous

INSERT INTO category (category, sub_category, rules)
VALUES ('Rowing', 'Maddy', '{"column":"payee","operation":"equals","value":"EGGS rowing"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('School', 'Maddy', '{"column":"payee","operation":"equals","value":"EPSOM GIRLS GRA"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Home', 'Bunnings', '{"column":"payee","operation":"contains","value":"Bunnings"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Home', 'Mitre 10', '{"column":"payee","operation":"contains","value":"Mitre 10"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Pool', 'Pool', '{"column":"payee","operation":"equals","value":"The Pool People Ltd    Remuera       Nz"}');

-- Simon

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Alcohol', '{"column":"payee","operation":"contains","value":"Gs Cellar"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Alcohol', '{"column":"payee","operation":"equals","value":"Liquorland Newmarket   Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Alcohol', '{"column":"payee","operation":"equals","value":"Greenlane Liquor Ctr   Greenlane Auc Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Alcohol', '{"column":"payee","operation":"equals","value":"Epsom Liquor           Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Alcohol', '{"column":"payee","operation":"contains","value":"Liquor"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Alcohol', '{"column":"payee","operation":"contains","value":"The Lumsden"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"equals","value":"Browning Automotive    Auckland      Nzl"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"equals","value":"Nz Transport Agency    Palmerston No Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"equals","value":"Washdepot Greenlane Lt Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"equals","value":"Trademe - Motorweb     Auk           Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"equals","value":"A-Nz Auto Ass"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"contains","value":"Repco"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"equals","value":"A1 Onehunga Towing     Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"equals","value":"Aa Battery Service     Auckland      Nzl"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Car', '{"column":"payee","operation":"equals","value":"Aa Vehicle Testing     Glen Innes    Nzl"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Cornwall Park Supere"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"contains","value":"Taco Joint Akld Uni"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Gourmet Delicious Li"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Hello Mister Parnell"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Fish And Chip Shop E"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Sumthin Dumplin        Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Hell Pizza Epsom       Auckland      Nzl"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Sachie''S Kitchen"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Hilltop Superette"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Goodness Gracious"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Podium"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"contains","value":"Rice Kitchen"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"contains","value":"Bakery"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"contains","value":"Cafe Cuba"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"contains","value":"McDonalds"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"contains","value":"Mcdonalds"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"contains","value":"Fish And Chip"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"contains","value":"Kk Malaysian"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Mcdonalds Greenlane    Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Casa Del Gelato"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Hobson Indian Takeaw"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Atomic Coffee Roasters Auckland      Nzl"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Better Burger Mt Ede"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Better Burger Vulcan L Auckland Cbd  Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Namaste Delhi          Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Eating', '{"column":"payee","operation":"equals","value":"Namaste Delhi"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Gym', '{"column":"payee","operation":"equals","value":"Cityfitness Group"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Gym', '{"column":"payee","operation":"equals","value":"Jetts Fitness"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Health', '{"column":"payee","operation":"equals","value":"Lumino The Dentists    Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Lotto', '{"column":"payee","operation":"equals","value":"Mylotto.Co.Nz          New Zealand   Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Kung Fu', '{"column":"payee","operation":"equals","value":"Kung Fu"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Parking', '{"column":"payee","operation":"contains","value":"Civic Car Park"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Parking', '{"column":"payee","operation":"contains","value":"Smales Farm Parking"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Parking', '{"column":"payee","operation":"contains","value":"Wilson Parking"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Parking', '{"column":"payee","operation":"equals","value":"Akld Transport Parking Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Parking', '{"column":"payee","operation":"equals","value":"Akl Airport Carpark    Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Petrol', '{"column":"payee","operation":"contains","value":"Bp 2Go"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Petrol', '{"column":"payee","operation":"contains","value":"Caltex"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Petrol', '{"column":"payee","operation":"contains","value":"Z "}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Petrol', '{"column":"payee","operation":"equals","value":"Kiwi Fuels Ltd         Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Petrol', '{"column":"payee","operation":"equals","value":"Bp Connect Boulevard   Auckland      Nzl"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Rowing', '{"column":"payee","operation":"equals","value":"Auckland Rowing Club"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Spending', '{"column":"payee","operation":"equals","value":"4835-****-****-0768  Df"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Spending', '{"column":"payee","operation":"equals","value":"4835-****-****-0768  Nf"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Spending', '{"column":"payee","operation":"equals","value":"4835-****-****-9087  Df"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Spending', '{"column":"payee","operation":"equals","value":"4835-****-****-9087  Nf"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Spending', '{"column":"payee","operation":"equals","value":"4921-****-****-8523"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Spending', '{"column":"payee","operation":"contains","value":"Ticketmaster"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Spending', '{"column":"payee","operation":"contains","value":"Steamgames"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Tech', '{"column":"payee","operation":"equals","value":"PBTech"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Tech', '{"column":"payee","operation":"equals","value":"Pb Tech Online 09 5269 Penrose       Nzl"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Tech', '{"column":"payee","operation":"equals","value":"Pb Technologies Penr"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Tech', '{"column":"payee","operation":"equals","value":"Aliexpress.Com"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Tech', '{"column":"payee","operation":"equals","value":"Jaycar Pty Ltd         Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Travel', '{"column":"payee","operation":"equals","value":"Uber Trip Help.Uber.Co Vorden        Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Travel', '{"column":"payee","operation":"equals","value":"Uber   *Trip           Help.Uber.Com Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Travel', '{"column":"payee","operation":"equals","value":"Lim*Ride Cost          Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Travel', '{"column":"payee","operation":"equals","value":"Air Nz One             Auckland      Nz"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Travel', '{"column":"payee","operation":"equals","value":"Mt Eden Cycles         Auckland      Nzl"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Web', '{"column":"payee","operation":"equals","value":"Amazon Web Services    Aws.Amazon.Co Wa"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Web', '{"column":"payee","operation":"equals","value":"Google *Google Storage G.Co/Helppay# Gb"}');

INSERT INTO category (category, sub_category, rules)
VALUES ('Simon', 'Web', '{"column":"payee","operation":"equals","value":"Google  Google Storage Auckland      Nz"}');
