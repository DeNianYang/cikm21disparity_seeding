#for k in 5000
# do
# 	# for the agnostic
# 	./Diffusion ${1} agnostic-${2}-${k}.csv ${k} >> tmp &
# 	# # # for the parity
# 	# ./Diffusion ${1} parity-${2}-${k}.csv ${k} >> tmp &
	
# done

for ratio in 0.0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 1.0
# for ratio in 0.4
do
	# for k in 1 2 5 10 20 50 100 200 500 1000
	# for k in 5000
	for k in 100
	do
		# # for the agnostic
		 ./Diffusion ${1} ../dataset/target_hindex-${2}-${k}-${ratio}.csv ${k} >> tmp &
		# for the diversity train
		#time ./Diffusion ${1} diversity-${2}-${k}-${ratio}.csv ${k} >> tmp &
		# # for the diversity test
		# ./Diffusion ${1} diversity-${2}-${k}-${ratio}.csv 10000 >> tmp &
	done
done
