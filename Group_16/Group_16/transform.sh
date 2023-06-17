for number in $(seq 1 10)
do
    echo "Number: $number"
    python transform.py --txt_path ./Task_2_COS_chatGPT_output/$number.txt --json_path ./Task_2_COS_result/$number.json
done

for number in $(seq 1 10)
do
    echo "Number: $number"
    python transform.py --txt_path ./Task_2_FOOD_chatGPT_output/$number.txt --json_path ./Task_2_FOOD_result/$number.json
done

for number in $(seq 1 10)
do
    echo "Number: $number"
    python transform.py --txt_path ./Task_2_MED_chatGPT_output/$number.txt --json_path ./Task_2_MED_result/$number.json
done

