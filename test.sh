for i in 'yunnansheng' 'jilinsheng' 'anhuisheng' 'shandongsheng' 'shaanxisheng' 'guangdongsheng' 'jiangsusheng' 'jiangxisheng' 'henansheng' 'zhejiangsheng' 'hubeisheng' 'hunansheng' 'fujiansheng' 'guizhousheng' 'liaoningsheng' 'shanxisheng' 'heilongjiang'
do
	PGPASSWORD=123 psql -h localhost -d postgres -U postgres -c 'CREATE SCHEMA '$i''
done