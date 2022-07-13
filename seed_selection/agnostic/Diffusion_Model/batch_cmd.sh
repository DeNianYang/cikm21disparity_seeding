#for k in 5000
# do
# 	# for the agnostic
# 	./Diffusion ${1} agnostic-${2}-${k}.csv ${k} >> tmp &
# 	# # # for the parity
# 	# ./Diffusion ${1} parity-${2}-${k}.csv ${k} >> tmp &
	
# done

for ratio in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
# for ratio in 0.4
do
	# for k in 1 2 5 10 20 50 100 200 500 1000
	# for k in 5000
	for k in 5 10 20 50 100
	do
		# # for the agnostic
		 ./Diffusion ${1} ../dataset/agnostic-${2}-${k}-${ratio}.csv ${k} >> tmp &
		# for the diversity train
		#time ./Diffusion ${1} diversity-${2}-${k}-${ratio}.csv ${k} >> tmp &
		# # for the diversity test
		# ./Diffusion ${1} diversity-${2}-${k}-${ratio}.csv 10000 >> tmp &
	done
done
