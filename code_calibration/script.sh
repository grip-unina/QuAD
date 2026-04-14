echo AncesTree uncalibrated
python evaluate.py ../data_AncesTree/AncesTree_test.csv
echo -e "--------------------------\n\n"

echo AncesTree calibrated
python calibration.py --dev_set_csv ../data_AncesTree/AncesTree_dev.csv --eval_set_csv ../data_AncesTree/AncesTree_test.csv --output_csv out.csv
python evaluate.py out.csv
echo -e "--------------------------\n\n"

echo ReWIND uncalibrated
python evaluate.py ../data_ReWIND/ReWIND.csv
echo -e "--------------------------\n\n"

echo ReWIND calibrated
python calibration.py --dev_set_csv ../data_AncesTree/AncesTree_dev.csv --eval_set_csv ../data_ReWIND/ReWIND.csv --output_csv out.csv
python evaluate.py out.csv
echo -e "--------------------------\n\n"

echo ReWIND calibrated LOO
python calibration_LOO.py --eval_set_csv ../data_ReWIND/ReWIND.csv --output_csv out.csv
python evaluate.py out.csv
echo -e "--------------------------\n\n"

