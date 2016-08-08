# -*- coding: UTF-8 -*-
import json
import logging
import string

from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response

from loadtest.froms import VexLoadTestInsertionForm
from loadtest.models import LoadTestResult, get_test_type_json_list, \
    get_test_version_json_list, get_test_module_json_list
from loadtest.util import get_current_day_start_date

logger = logging.getLogger(__name__)

def page_not_found(request):
    return render_to_response('404.html')

def page_error(request):
    return render_to_response('500.html')

# 关于
# @cache_page(60 * 60 * 24)
def about(request):
    return render(request, 'loadtest/about.html')

# 展示最新的压力测试结果
# @cache_page(60 * 15)
def show_latest(request):
    context = {}
    
    # List = [{'color': '#FF0F00', 'Client': '7217', 'ResponseTime': '0-20'}, {'color': '#FF6600', 'Client': '288474', 'ResponseTime': '20-50'}, ];
    lastest_load_test_result = LoadTestResult.objects.latest(field_name='test_date');
    index_result = _get_armcharts_column_list(lastest_load_test_result.test_result_index)
    bitrate_result = _get_armcharts_column_list(lastest_load_test_result.test_result_bitrate)
    
    index_benchmark_summary = _get_benchmark_number(lastest_load_test_result.test_result_index, '_index', lastest_load_test_result.test_instance_number)
    bitrate_benchmark_summary = _get_benchmark_number(lastest_load_test_result.test_result_bitrate, '_bitrate', lastest_load_test_result.test_instance_number)
    
    context.update(lastest_load_test_result.as_dict())
    context.update({'index_result_json': json.dumps(index_result), 'bitrate_result_json': json.dumps(bitrate_result), })
    context.update(index_benchmark_summary)
    context.update(bitrate_benchmark_summary)
    
    logger.debug("Context is: %s", context)
    return render(request, 'loadtest/latestResult.html', context)

# 显示所有的压力测试类型。如果参数中包含测试类型，则显示最近10次的压力测试数据时间
def show_all_load_test_results(request, test_type=None):
    if test_type is not None:
        logger.debug("Show all %s test results", test_type)
    else:
        logger.debug("Show all test results for both linear/vod/cdvr")
    
    load_test_results = LoadTestResult.objects.all()[0:10] if test_type is None else LoadTestResult.objects.filter(test_type=test_type);
    context = {} if test_type is None else {'selected_test_type': test_type}
    context.update({'test_type_list': get_test_type_json_list(),
                    'test_version_list': get_test_version_json_list(),
                    'test_module_list': get_test_module_json_list(), })
    
    if len(load_test_results) > 0:
        latest_load_test_result = load_test_results[0]
        index_results = _get_armcharts_column_list(latest_load_test_result.test_result_index)
        bitrate_results = _get_armcharts_column_list(latest_load_test_result.test_result_bitrate)
        
        index_benchmark_summary = _get_benchmark_number(latest_load_test_result.test_result_index, '_index')
        bitrate_benchmark_summary = _get_benchmark_number(latest_load_test_result.test_result_bitrate, '_bitrate')
        
        context.update({'load_test_results':load_test_results,
                        'selected_test_id': latest_load_test_result.id,
                        'selected_test_module':latest_load_test_result.test_module,
                        'selected_test_version':latest_load_test_result.test_version,
                       'index_result_json': json.dumps(index_results),
                       'bitrate_result_json': json.dumps(bitrate_results),
                       })
        context.update(latest_load_test_result.as_dict())
        context.update(index_benchmark_summary)
        context.update(bitrate_benchmark_summary)
        
    logger.debug("Context is: %s", context)
    return render(request, 'loadtest/testResults.html', context)

# 显示某一次压力测试结果. 默认缓存5分钟
# @cache_page(60 * 5 * 1)
def show_one_load_test_result(request, test_id):
    logger.debug("Show test results for test_id: %s", test_id)
    
    load_test_result = LoadTestResult.objects.get(id=test_id);
    load_test_results = LoadTestResult.objects.filter(test_version=load_test_result.test_version, test_type=load_test_result.test_type, test_module=load_test_result.test_module);
    
    context = {}
    
    index_results = _get_armcharts_column_list(load_test_result.test_result_index)
    bitrate_results = _get_armcharts_column_list(load_test_result.test_result_bitrate)
    index_benchmark_summary = _get_benchmark_number(load_test_result.test_result_index, '_index')
    bitrate_benchmark_summary = _get_benchmark_number(load_test_result.test_result_bitrate, '_bitrate')
        
    context.update({'load_test_results':load_test_results,
                    'index_result_json': json.dumps(index_results),
                    'bitrate_result_json': json.dumps(bitrate_results),
                    'selected_test_version':load_test_result.test_version,
                    'selected_test_id':test_id,
                    'selected_test_module':load_test_result.test_module,
                    'test_type_list': get_test_type_json_list(),
                    'test_version_list': get_test_version_json_list(),
                    'test_module_list': get_test_module_json_list(),
                    })
    context.update(load_test_result.as_dict())
    context.update(index_benchmark_summary)
    context.update(bitrate_benchmark_summary)
    logger.debug("Context is: %s", context)
    return render(request, 'loadtest/testResults.html', context)

# 获取所有的压力测试结果信息
def get_all_load_test_results_by_version(request, test_type, test_version):
    loadtest_results = LoadTestResult.objects.filter(test_type=test_type, test_version=test_version);
    results = [ob.as_dict() for ob in loadtest_results]
    logger.debug("Load test result for %s-%s is %s", test_type, test_version, str(results))
    return HttpResponse(json.dumps(results), content_type="application/json")

def get_all_load_test_results_by_module(request, test_type, test_version, test_module):
    loadtest_results = LoadTestResult.objects.filter(test_type=test_type, test_version=test_version, test_module=test_module);
    results = [ob.as_dict() for ob in loadtest_results]
    logger.debug("Load test result for %s is %s", test_version, str(results))
    return HttpResponse(json.dumps(results), content_type="application/json")

# 插入一条压力测试结果(通过form验证)
def insert_test_result_with_form(request):
    try:
        if request.method == 'POST':
            
            # 标准的从网页提交的数据会直接被django将数据转换到了requst.POST中，表现为QueryDict. 
            # form = VexLoadTestInsertionForm(request.POST)
            # 我们这里是从request body中post过去的，因此需要转换request.body中的数据到dict，才能使用form的validation
            # 且validation要求UI上的post对象的名称和model中的对象的名称完全一致。因此需要转换index_results和bitrate_results为test_result_index和test_result_bitrate
            data = request.POST if request.POST else convert_request_body_to_form_validation(request.body)
            form = VexLoadTestInsertionForm(data)
            errors = {}
            # 验证表单是否正确
            if form.is_valid():
                form.save()
                return HttpResponse("Test result has been saved.")
            else:
                errors.update(form.errors)
                return HttpResponse(json.dumps({"errors": errors}), content_type="application/json", status=400)
        else:   
            return HttpResponse("Request must be posted with XML body", status=400)
    except Exception, e:
        logger.error(e)
        return HttpResponse(e.message, status=400)

# 插入一条压力测试结果(不通过form验证)
def insert_test_result(request):
    if request.method == 'POST':
        logger.debug("insert load test request with body:" + request.body)
        data = request.POST if request.POST else convert_request_body_to_form_validation(request.body)
        test_date = get_current_day_start_date() if data['test_date'] is None else get_current_day_start_date(data['test_date'])
        
        try:
            exist_test_result = get_object_or_404(LoadTestResult, test_date=test_date, test_type=data['test_type'], test_version=data['test_version'])
            logger.info("Test result for %s[%s][%s] is existed, just update it", data['test_type'], data['test_version'], test_date)
            
            exist_test_result.test_result_bitrate = data['test_result_bitrate']
            exist_test_result.test_result_error = data['test_result_error']
            exist_test_result.test_result_index = data['test_result_index']
            exist_test_result.save()
            return HttpResponse("Test result has been updated.")
        except:
            # 这里没有验证。如果需要验证，可以采用form验证的方式
            result = LoadTestResult()
            result.test_type = data['test_type']
            result.test_version = data['test_version']
            result.test_date = test_date
            result.test_result_index = data['test_result_index']
            result.test_result_bitrate = data['test_result_bitrate']
            result.test_result_error = data['test_result_error']
            result.save()
            return HttpResponse("Test result has been saved.")
    else:   
        return HttpResponse("Must be post with XML body", status=400)

def _get_armcharts_column_list(benchmark_result):
    convert_column_list = []
    for line in benchmark_result.split('\n'):
        if string.strip(line) == '':
            continue
        
        converted_dict = {}
        client_number = line.split(':')[1].replace('\r', '')
        
        if line.find('error') > 0:
            converted_dict['ResponseTime'] = '12000+'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#CD0D74'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('0    ~ 20   milliseconds') > 0:
            converted_dict['ResponseTime'] = '0-20'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#FF0F00'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('20   ~ 50   milliseconds') > 0:
            converted_dict['ResponseTime'] = '20-50'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#FF6600'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('50   ~ 200  milliseconds') > 0:
            converted_dict['ResponseTime'] = '50-200'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#FF9E01'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('200  ~ 500  milliseconds') > 0:
            converted_dict['ResponseTime'] = '200-500'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#FCD202'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('500  ~ 1000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '500-1000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#F8FF01'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('1000 ~ 2000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '1000-2000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#B0DE09'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('2000 ~ 3000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '3000-3000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#04D215'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('3000 ~ 4000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '3000-4000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#0D8ECF'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('4000 ~ 5000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '4000-5000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#0D52D1'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('5000 ~ 6000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '5000-6000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#2A0CD0'
            convert_column_list.append(converted_dict)
            continue
        
        if line.find('6000 ~ 12000 milliseconds') > 0:
            converted_dict['ResponseTime'] = '6000-12000'
            converted_dict['Client'] = client_number
            converted_dict['color'] = '#8A0CCF'
            convert_column_list.append(converted_dict)
            continue
        
    final_convert_column_list = convert_column_list[1:-1] + [convert_column_list[0]]
    return final_convert_column_list

def _get_benchmark_number(benchmark_result, tag='', instance_number=2):
    average_response = 0
    benchmark_time = 0
    request_number = 0
    error_number = 0
    
    for line in benchmark_result.split('\n'):
        if string.strip(line) == '':
            continue
        
        m_number = line.split(':')[1].replace('\r', '')
        if line.find('error') > 0:
            error_number = int(m_number)
            continue
        
        if line.find('Average response') > 0:
            average_response = int(m_number)
            continue
        
        if line.find('Total request') > 0:
            request_number = int(m_number)
            continue
        
        if line.find('Total cost') > 0:
            benchmark_time = int(m_number)
            continue
    
    results = {"average_response":0, "benchmark_time":0, "concurrent_session":0, "error_rate":0}
    results["average_response" + tag] = average_response
    results["benchmark_time" + tag] = "{} hour {} minutes".format(str(benchmark_time / 3600), str((59 + benchmark_time - 3600 * (benchmark_time / 3600)) / 60))
    results["concurrent_session" + tag] = ((request_number / benchmark_time) + 1) / instance_number
    results["error_rate" + tag] = round((float(error_number) / request_number) * 100, 2)
    return results

def convert_request_body_to_form_validation(request_body):
    logger.debug("convert load test insertion request body:" + request_body)
    '''
    <?xml version="1.0"?>
        <loadtest_data>
            <index_results>
            Index request report:
              Average response (milliseconds):23
              Total cost time             :5419
              Total request number        :1082677
              Total response error number :0
                0    ~ 20   milliseconds :550512
                20   ~ 50   milliseconds :470302
                50   ~ 200  milliseconds :60111
                200  ~ 500  milliseconds :1447
                500  ~ 1000 milliseconds :114
                1000 ~ 2000 milliseconds :191
                2000 ~ 3000 milliseconds :0
                3000 ~ 4000 milliseconds :0
                4000 ~ 5000 milliseconds :0
                5000 ~ 6000 milliseconds :0
                6000 ~ 12000 milliseconds :0
            </index_results>
            <bitrate_results>
            Bit rate request report:
              Average response (milliseconds):23
              Total cost time             :5419
              Total request number        :1082677
              Total response error number :0
                0    ~ 20   milliseconds :550512
                20   ~ 50   milliseconds :470302
                50   ~ 200  milliseconds :60111
                200  ~ 500  milliseconds :1447
                500  ~ 1000 milliseconds :114
                1000 ~ 2000 milliseconds :191
                2000 ~ 3000 milliseconds :0
                3000 ~ 4000 milliseconds :0
                4000 ~ 5000 milliseconds :0
                5000 ~ 6000 milliseconds :0
                6000 ~ 12000 milliseconds :0
            </bitrate_results>
            <error_results>
            3333333333333333
            </error_results>
            <test_type>VOD</test_type>
            <test_date>2017-01-08 00:00:00</test_date>
            <test_version>2.7</test_version>
        </loadtest_data>
    '''
    
    try:
        import xml.etree.ElementTree as ET
        root = ET.XML(request_body)
        bitrate_results_element = root.find('bitrate_results')
        index_results_element = root.find('index_results')
        error_results_element = root.find('error_results')
        test_type_element = root.find('test_type')
        test_version_element = root.find('test_version')
        test_date_element = root.find('test_date')
        
        data = {}
        data['test_type'] = _clear_data(test_type_element.text) if test_type_element is not None else ''
        data['test_version'] = _clear_data(test_version_element.text) if test_version_element is not None else ''
        data['test_result_index'] = _clear_data(index_results_element.text) if index_results_element is not None else ''
        data['test_result_bitrate'] = _clear_data(bitrate_results_element.text) if bitrate_results_element is not None else ''
        data['test_result_error'] = _clear_data(error_results_element.text) if error_results_element is not None else ''
        data['test_date'] = _clear_data(test_date_element.text) if error_results_element is not None else None
        logger.debug("Converted form data is:" + str(data))
        return data
    except Exception, e:
        logger.error(e)
        raise Exception('Parsing XML failed, please check XML content in body.\nXML content is:\n' + request_body)

def _clear_data(data):
    data = data.strip()
    return data
