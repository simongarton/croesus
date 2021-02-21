rm -rf build/
mkdir build
cp lambda.py build/
cp requirements.txt build/
cd build
pip3 install -r requirements.txt -t .
rm ../lambda.zip
zip -r ../lambda.zip .
cd ..
rm -rf build/
