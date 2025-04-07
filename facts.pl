serviceConnection(load_balancer, frontend, 0.0049999999999999906, 4.99999999999999).
serviceConnection(frontend, api, 0.0049999999999999906, 4.99999999999999).
serviceConnection(frontend, redis, 0.003, 3.0).
serviceConnection(api, identity_provider, 0.003, 3.0).
serviceConnection(api, etcd, 0.004000000000000005, 4.000000000000005).
serviceConnection(api, database, 0.01100000000000002, 11.00000000000002).
serviceConnection(api, redis, 0.0010000000000000013, 1.0000000000000013).
serviceConnection(identity_provider, etcd, 0.0010000000000000013, 1.0000000000000013).
service(load_balancer, 0.747, 747.0).
service(frontend, 0.594, 594.0).
service(api, 1.2274449947122323, 1227.4449947122323).
service(identity_provider, 0.8839999999999996, 883.9999999999995).
service(database, 1.360999999999997, 1360.999999999997).
service(redis, 0.08800000000000016, 88.00000000000016).
service(etcd, 0.045, 45.0).
node(public1, 402).
node(public2, 255).
node(private1, 346).
node(private2, 74).
node(private3, 620).
node(private4, 155).
node(private5, 290).
deployedTo(load_balancer,large,public1).
deployedTo(api,large,private1).
deployedTo(frontend,large,public1).
deployedTo(identity_provider,large,private3).
deployedTo(redis,large,private3).
deployedTo(database,large,private5).
deployedTo(etcd,large,private2).
highConsumptionConnection(api,large,database,large,0.006).
highConsumptionConnection(load_balancer,large,frontend,large,0.003).
highConsumptionService(api,large,private3,0.910).
highConsumptionService(database,large,private3,1.000).
