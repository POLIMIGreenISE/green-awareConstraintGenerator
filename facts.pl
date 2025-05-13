serviceConnection(checkoutservice, currencyservice, 0.15055450974592705, 150.55450974592705).
serviceConnection(checkoutservice, emailservice, 0.23004448351285184, 230.04448351285183).
serviceConnection(checkoutservice, paymentservice, 0.0633326774234186, 63.332677423418595).
serviceConnection(checkoutservice, productcatalogservice, 0.09039252254201993, 90.39252254201993).
serviceConnection(checkoutservice, shippingservice, 0.22293258040013347, 222.93258040013347).
serviceConnection(frontend, productcatalogservice, 4.789738099724981, 4789.738099724981).
serviceConnection(frontend, recommendationservice, 1.4389770393771097, 1438.9770393771098).
serviceConnection(frontend, shippingservice, 0.3330412962143404, 333.04129621434043).
serviceConnection(frontend, adservice, 0.7051560446875358, 705.1560446875358).
serviceConnection(checkoutservice, cartservice, 0.11736729982468017, 117.36729982468016).
serviceConnection(frontend, cartservice, 1.5218598419506317, 1521.8598419506318).
serviceConnection(frontend, checkoutservice, 0.15787649658515154, 157.87649658515156).
serviceConnection(frontend, currencyservice, 3.189833469713948, 3189.833469713948).
serviceConnection(recommendationservice, productcatalogservice, 0.5355739038179307, 535.5739038179307).
service(frontend, 2.861262, 2861.262).
service(productcatalogservice, 1.277202, 1277.202).
service(currencyservice, 1.137168, 1137.168).
service(recommendationservice, 0.778833, 778.833).
service(cartservice, 0.705945, 705.945).
service(adservice, 0.324624, 324.624).
service(checkoutservice, 0.15506999999999999, 155.07).
service(shippingservice, 0.127671, 127.671).
service(emailservice, 0.06540900000000001, 65.409).
service(paymentservice, 0.045117, 45.117).
node(france, 16).
node(spain, 88).
node(germany, 132).
node(greatbritain, 213).
node(italy, 335).
deployedTo(frontend,large,france).
deployedTo(productcatalogservice,large,greatbritain).
deployedTo(recommendationservice,large,germany).
deployedTo(checkoutservice,tiny,spain).
deployedTo(adservice,tiny,germany).
deployedTo(cartservice,tiny,greatbritain).
deployedTo(shippingservice,tiny,greatbritain).
deployedTo(currencyservice,tiny,greatbritain).
deployedTo(paymentservice,tiny,italy).
deployedTo(emailservice,tiny,italy).
highConsumptionConnection(frontend,large,productcatalogservice,large,0.572).
highConsumptionConnection(frontend,large,currencyservice,tiny,0.381).
highConsumptionService(frontend,large,greatbritain,0.636).
highConsumptionService(frontend,large,italy,1.000).
highConsumptionService(productcatalogservice,large,italy,0.446).
