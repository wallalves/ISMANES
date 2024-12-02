from Logger import Logger

logger = Logger()
logger.log("Este é um log de exemplo.",logger.logtype_info)
logger.log("Este é um aviso.", logger.logtype_warning)
logger.log("Este é um erro crítico!", logger.logtype_error)