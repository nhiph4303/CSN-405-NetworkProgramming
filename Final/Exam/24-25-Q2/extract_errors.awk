BEGIN {
    # In tiêu đề trước khi xử lý các dòng
    print "Date Time"
}

# Nếu cột số 3 (Level) là ERROR thì in ra cột 1 (Date) và cột 2 (Time)
$3 == "ERROR" {
    print $1 " " $2
}
