import requests

url = 'http://localhost:8000/gender_decoder'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
data = {
  "job_description": "Slalom is a purpose-driven consulting firm that helps companies solve business problems and build for the future, with solutions spanning business advisory, customer experience, technology, and analytics. We partner with companies to push the boundaries of what?s possible?together. Founded in 2001 and headquartered in Seattle, WA, Slalom has organically grown to nearly 4,000 employees. We were named one of Fortune?s 100 Best Companies to Work For in 2016 and are regularly recognized by our employees as a best place to work. You can find us in 25 cities across the U.S., U.K., and Canada. Job Title: .NET Developer Our Architecture and Development Practice is interested in adding talented, experienced developers to its team. As a consultant, you will be involved in designing and delivering quality solutions. Your duties may include interacting with the user or business group to help define the client*s needs and translating those needs into a solution of value. As a partner to our client, you will help them be successful by working within their framework or bringing an appropriate framework and structure to the process that works well with the client. Responsibilities: Design, develop, test, support, and deploy desktop, custom web, and mobile applications in a .NET environment Develop system architecture, design, and code in accordance with the clients' requirements Help architect and design solutions, or act in a lead position responsible for the productivity of the development team Help clients implement software development methodologies Produce applications that provide measurable business value to our clients Qualifications: 3+ years of development experience, and a minimum of 2 years of experience with Microsoft Visual Studio, C# or Visual Basic, and ASP.Net Experience with object-oriented design and development techniques; solid understanding of basic development best practices Ability to work well in a team and individually Azure experience strongly preferred Formal training or experience in project management and building a rapport with clients Demonstrated ability around decision-making, delegation, and building trust and credibility Understanding of how software development projects are organized, including how work is prioritized, scope-managed, and risk-assessed and mitigated Slalom is an equal opportunity employer and all qualified applicants will receive consideration for employment without regard to race, color, religion, sex, national origin, disability status, protected veteran status, or any other characteristic protected by law."
}

r = requests.post(
    url=url,
    headers=headers,
    json=data
    )

status_code = r.status_code
gender_decoder_result = r.json()['gender_decoder_result']

print(f'Status: {status_code}\nJSON: {gender_decoder_result}')
