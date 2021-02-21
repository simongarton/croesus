aws dynamodb create-table \
    --table-name stock_price \
    --attribute-definitions \
        AttributeName=exchange,AttributeType=S \
        AttributeName=symbol,AttributeType=S \
    --key-schema \
        AttributeName=exchange,KeyType=HASH \
        AttributeName=symbol,KeyType=RANGE \
--provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5