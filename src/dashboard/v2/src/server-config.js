const public_ip = require('public-ip');
const USELOCAL=true;

module.exports.getIp= async (options) =>  {
	options = {
		...options
  };
  
  //all Env are strings, so cant do strict typing
  if(USELOCAL){
    return 'localhost';
  }

	return (await public_ip.v4());
};
