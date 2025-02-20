serviceConnection(checkoutservice, currencyservice, 26.030874735070782, 97.86043133485256).
serviceConnection(checkoutservice, emailservice, 39.77469119937208, 149.52891428335369).
serviceConnection(checkoutservice, paymentservice, 10.950219926509076, 41.16624032522209).
serviceConnection(checkoutservice, productcatalogservice, 15.628867147515244, 58.75513965231294).
serviceConnection(checkoutservice, shippingservice, 38.54504315118307, 144.90617726008674).
serviceConnection(frontend, productcatalogservice, 168.11980730034682, 3113.3297648212374).
serviceConnection(frontend, recommendationservice, 50.50809408213656, 935.3350755951215).
serviceConnection(frontend, shippingservice, 11.689749497123351, 216.47684253932132).
serviceConnection(frontend, adservice, 24.750977168532504, 458.35142904689826).
serviceConnection(checkoutservice, cartservice, 20.2928061396872, 76.28874488604211).
serviceConnection(frontend, cartservice, 53.417280452467175, 989.2088972679106).
serviceConnection(frontend, checkoutservice, 5.54146503013882, 102.61972278034852).
serviceConnection(frontend, currencyservice, 111.96315478695956, 2073.391755314066).
serviceConnection(recommendationservice, productcatalogservice, 92.60072797012022, 348.123037481655).
service(frontend, 213.60703603408226, 3955.685852483005).
service(productcatalogservice, 469.6835971873102, 1765.7278089748504).
service(currencyservice, 532.9524895865102, 1572.1312377183192).
service(recommendationservice, 286.4112998947577, 1076.734210130668).
service(cartservice, 330.8527370284329, 975.9667758950823).
service(adservice, 152.14037765706678, 448.79167450462177).
service(checkoutservice, 57.026089385888994, 214.3837946837932).
service(shippingservice, 59.8351143349086, 176.50476204987788).
service(emailservice, 30.655003826491825, 90.42773990115582).
service(paymentservice, 21.144824223575213, 62.37411275390919).
node(node_a, 27).
node(node_b, 35).
node(node_c, 25).
deployedTo(frontend,large,node_a).
deployedTo(productcatalogservice,medium,node_b).
deployedTo(recommendationservice,large,node_b).
deployedTo(checkoutservice,large,node_b).
deployedTo(adservice,small,node_c).
deployedTo(cartservice,small,node_c).
deployedTo(shippingservice,small,node_c).
deployedTo(currencyservice,small,node_c).
deployedTo(paymentservice,small,node_c).
deployedTo(emailservice,small,node_c).
highConsumptionConnection(frontend,large,productcatalogservice,medium,0.315).
highConsumptionConnection(frontend,large,currencyservice,small,0.210).
highConsumptionConnection(recommendationservice,large,productcatalogservice,medium,0.130).
highConsumptionConnection(frontend,large,cartservice,small,0.075).
highConsumptionConnection(frontend,large,recommendationservice,large,0.071).
highConsumptionService(productcatalogservice,medium,node_b,0.881).
highConsumptionService(currencyservice,small,node_a,1.000).
highConsumptionService(currencyservice,small,node_b,1.000).
highConsumptionService(currencyservice,small,node_c,1.000).
