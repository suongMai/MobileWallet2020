"""
	@author: Suong.Mai
"""


from mobilewallet import create_app
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

application = create_app()

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=80,debug=True)
    
