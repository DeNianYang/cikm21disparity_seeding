Diffusion simulation

Command:
./Diffusion [network] [seed_file] [seed_number_k] [homophily_rho] [sampling_number]
* homophily_rho: optional, default = 1
* sampling_number: optional, default = 10,000

Example:
./Diffusion like hindexl 5

Run in batch:

source ./batch_cmd.sh like tprl
source ./batch_cmd.sh comment tprc


source ./batch_cmd.sh like indegreel
source ./batch_cmd.sh comment indegreec
source ./batch_cmd.sh like hindexl
source ./batch_cmd.sh comment hindexc
source ./batch_cmd.sh like frequencyl
source ./batch_cmd.sh comment frequencyc
source ./batch_cmd.sh like hiindexl
source ./batch_cmd.sh comment hiindexc
source ./batch_cmd.sh like pagerankl
source ./batch_cmd.sh comment pagerankc

source ./batch_cmd.sh like frequencyl
source ./batch_cmd.sh comment frequencyc
source ./batch_cmd.sh like hiindexl
source ./batch_cmd.sh comment hiindexc
source ./batch_cmd.sh like pagerankl
source ./batch_cmd.sh comment pagerankc
