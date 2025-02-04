serviceConnection(checkoutservice, currencyservice, 27.49878120509357, 97.86043133485258).
serviceConnection(checkoutservice, emailservice, 42.01762491362239, 149.5289142833537).
serviceConnection(checkoutservice, paymentservice, 11.567713531387408, 41.16624032522209).
serviceConnection(checkoutservice, productcatalogservice, 16.51019424229994, 58.75513965231295).
serviceConnection(checkoutservice, shippingservice, 40.71863581008438, 144.90617726008676).
serviceConnection(frontend, productcatalogservice, 171.23313706516808, 3113.329764821238).
serviceConnection(frontend, recommendationservice, 51.44342915773168, 935.3350755951215).
serviceConnection(frontend, shippingservice, 11.90622633966267, 216.47684253932127).
serviceConnection(frontend, adservice, 25.2093285975794, 458.3514290468982).
serviceConnection(checkoutservice, cartservice, 21.437137312977832, 76.28874488604211).
serviceConnection(frontend, cartservice, 54.40648934973509, 989.2088972679107).
serviceConnection(frontend, checkoutservice, 5.644084752919169, 102.61972278034854).
serviceConnection(frontend, currencyservice, 114.03654654227364, 2073.3917553140664).
serviceConnection(recommendationservice, productcatalogservice, 97.82257353234505, 348.123037481655).
service(frontend, 217.56272188656527, 3955.685852483005).
service(productcatalogservice, 496.169514321933, 1765.7278089748504).
service(currencyservice, 528.2360958733552, 1572.1312377183192).
service(recommendationservice, 302.56231304671775, 1076.734210130668).
service(cartservice, 327.9248367007477, 975.9667758950823).
service(adservice, 150.7940026335529, 448.79167450462177).
service(checkoutservice, 60.24184630614589, 214.3837946837932).
service(shippingservice, 59.30560004875897, 176.50476204987788).
service(emailservice, 30.38372060678836, 90.42773990115582).
service(paymentservice, 20.957701885313487, 62.37411275390919).
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
highConsumptionConnection(frontend,large,productcatalogservice,medium,0.3241602351729884).
highConsumptionConnection(frontend,large,currencyservice,small,0.215881776033749).
highConsumptionConnection(recommendationservice,large,productcatalogservice,medium,0.18518721892832943).
highConsumptionService(productcatalogservice,medium, node_b, 0.9392949822968739).
highConsumptionService(currencyservice,small, node_b, 1.0).
