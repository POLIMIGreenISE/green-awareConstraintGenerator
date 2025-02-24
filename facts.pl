serviceConnection(checkoutservice, currencyservice, 0.07527725487296352, 75.27725487296352).
serviceConnection(checkoutservice, emailservice, 0.1150222417564259, 115.0222417564259).
serviceConnection(checkoutservice, paymentservice, 0.0316663387117093, 31.666338711709297).
serviceConnection(checkoutservice, productcatalogservice, 0.04519626127100996, 45.19626127100996).
serviceConnection(checkoutservice, shippingservice, 0.11146629020006674, 111.46629020006674).
serviceConnection(frontend, productcatalogservice, 2.3948690498624905, 2394.8690498624906).
serviceConnection(frontend, recommendationservice, 0.719488519688555, 719.488519688555).
serviceConnection(frontend, shippingservice, 0.1665206481071702, 166.52064810717022).
serviceConnection(frontend, adservice, 0.35257802234376784, 352.5780223437678).
serviceConnection(checkoutservice, cartservice, 0.05868364991234008, 58.68364991234008).
serviceConnection(frontend, cartservice, 0.760929920975316, 760.929920975316).
serviceConnection(frontend, checkoutservice, 0.07893824829257579, 78.93824829257579).
serviceConnection(frontend, currencyservice, 1.594916734856974, 1594.916734856974).
serviceConnection(recommendationservice, productcatalogservice, 0.26778695190896534, 267.78695190896536).
service(frontend, 2.832213905591043, 2832.213905591043).
service(productcatalogservice, 1.2642355941709256, 1264.2355941709257).
service(currencyservice, 1.1256232468725877, 1125.6232468725877).
service(recommendationservice, 0.7709261342488694, 770.9261342488694).
service(cartservice, 0.6987781075562003, 698.7781075562003).
service(adservice, 0.3213283533240181, 321.3283533240181).
service(checkoutservice, 0.15349569886994024, 153.49569886994024).
service(shippingservice, 0.12637485890516634, 126.37485890516633).
service(emailservice, 0.0647449549711996, 64.7449549711996).
service(paymentservice, 0.04465896334503833, 44.65896334503833).
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
highConsumptionConnection(frontend,large,productcatalogservice,medium,0.134).
highConsumptionConnection(frontend,large,currencyservice,small,0.067).
highConsumptionConnection(frontend,large,cartservice,small,0.032).
highConsumptionConnection(frontend,large,recommendationservice,large,0.030).
highConsumptionService(frontend,large,node_b,0.158).
highConsumptionService(frontend,large,node_c,0.158).
highConsumptionService(productcatalogservice,medium,node_c,0.355).
highConsumptionService(currencyservice,small,node_c,0.397).
