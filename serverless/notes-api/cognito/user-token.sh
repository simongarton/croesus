npx aws-api-gateway-cli-test \
--username='simon.garton@gmail.com' \
--password='Swordfish!XX1' \
--user-pool-id='ap-southeast-2_c8dxRL7kq' \
--app-client-id='7864qmfv1cvpa4apg5lb22cl02' \
--cognito-region='ap-southeast-2' \
--identity-pool-id='ap-southeast-2:b4e29b38-ddd7-48bc-912f-4235de44d7c9' \
--invoke-url='https://3w6ejhob7k.execute-api.ap-southeast-2.amazonaws.com/prod' \
--api-gateway-region='ap-southeast-2' \
--path-template='/notes' \
--method='POST' \
--body='{"content":"hello world","attachment":"hello.jpg"}'