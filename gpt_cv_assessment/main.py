def get_job_description():
    company = input('Enter company name > ').strip()
    job_title = input('Enter job title > ').strip()
    location = input('Enter job location > ').strip()
    notice_period = input('Enter notice period (if applicable) > ').strip()
    min_experience = input('Enter minimum years of experience > ').strip()
    max_experience = input('Enter maximum years of experience > ').strip()
    min_salary = input("Minimum salary offered (p.a): ").strip()
    max_salary = input("Maximum salary offered (p.a): ").strip()
    mandatory_skills = input('Enter the mandatory skills required for the job > ').strip()

    print("[Analyse JD] Important descriptions for the job (Enter 'STOP' when you are done):")
    desc_content = []
    while True:
        line = input().strip()
        if line.casefold() == 'stop'.casefold():
            break
        desc_content.append(line)
    print("[Analyse JD] Description uploaded")

    return dict(
        job_title=job_title, 
        company=company,
        location=location,
        notice_period = notice_period,
        mandatory_skills = mandatory_skills,
        job_description='\n'.join(desc_content), 
        min_experience=min_experience,
        max_experience=max_experience,
        salary_min = min_salary, salary_max=max_salary)


if __name__ == '__main__':
    import helper
    from openai import OpenAI
    from processors import JobRequirementProcessor, ResumeProcessor

    path = input('Enter resume path >').strip()
    rs_processor = ResumeProcessor()
    resume_data = rs_processor.read_document(path)

    openai_client = OpenAI()

    values = get_job_description()

    jd_processor = JobRequirementProcessor()
    requirements = jd_processor.process_reqirement(values)

    helper.save_to_json(requirements, 'jd_requirements.json')
    print('[JOB DESCRIPTION SUMMARY]\n', requirements)

    resume_data, _, _ = rs_processor.check_and_trim(resume_data)
    resume_summary = rs_processor.get_resume_summary(resume_data)

    helper.save_to_json(resume_summary, 'resume_summary.json')
    print('\n[RESUME SUMMARY]\n', resume_summary)
