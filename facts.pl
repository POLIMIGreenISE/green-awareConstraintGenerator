serviceConnection(checkoutservice, currencyservice, 26.226595597740488, 97.86043133485256).
serviceConnection(checkoutservice, emailservice, 40.07374902793879, 149.52891428335369).
serviceConnection(checkoutservice, paymentservice, 11.03255240715952, 41.166240325222084).
serviceConnection(checkoutservice, productcatalogservice, 15.746377426819869, 58.75513965231294).
serviceConnection(checkoutservice, shippingservice, 38.834855505703246, 144.90617726008674).
serviceConnection(frontend, productcatalogservice, 165.0064775355256, 3113.329764821238).
serviceConnection(frontend, recommendationservice, 49.57275900654144, 935.3350755951216).
serviceConnection(frontend, shippingservice, 11.473272654584028, 216.4768425393213).
serviceConnection(frontend, adservice, 24.292625739485604, 458.3514290468982).
serviceConnection(checkoutservice, cartservice, 20.445383629459286, 76.28874488604211).
serviceConnection(frontend, cartservice, 52.42807155519927, 989.2088972679107).
serviceConnection(frontend, checkoutservice, 5.438845307358472, 102.61972278034852).
serviceConnection(frontend, currencyservice, 109.88976303164551, 2073.3917553140664).
serviceConnection(recommendationservice, productcatalogservice, 93.29697404508353, 348.123037481655).
service(frontend, 96.34661726876033, 1817.860703184157).
service(productcatalogservice, 217.46900050465868, 811.4514944203682).
service(currencyservice, 241.30930642478253, 722.4829533676124).
service(recommendationservice, 132.61178268593756, 494.82008464902077).
service(cartservice, 149.80293001917317, 448.5117665244706).
service(adservice, 68.88585704912433, 206.24508098540218).
service(checkoutservice, 26.40374655556241, 98.52144237150152).
service(shippingservice, 27.092039575997934, 81.11389094610159).
service(emailservice, 13.879919610768683, 41.5566455412236).
service(paymentservice, 9.57391693924461, 28.664421973786254).
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
highConsumptionConnection(frontend,large,productcatalogservice,medium,0.6837965761878274).
highConsumptionConnection(frontend,large,currencyservice,small,0.4553896600995734).
highConsumptionConnection(recommendationservice,large,productcatalogservice,medium,0.38662816377604037).
highConsumptionService(productcatalogservice,medium, node_b, 0.9012043659925938).
highConsumptionService(currencyservice,small, node_b, 1.0).
